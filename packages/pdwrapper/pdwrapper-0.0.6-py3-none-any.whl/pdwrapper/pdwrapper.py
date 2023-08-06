import click
import logging
import sys,os
import yaml
import jsonschema
import subprocess
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

##############################################
# Global Variables
##############################################
aws_profile = os.getenv('AWS_PROFILE')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
git_branch = os.getenv('GITHUB_REF_NAME', '')
git_commit = os.getenv('GITHUB_SHA', '')
git_author = os.getenv('GITHUB_ACTOR', '')

allowed_app_types = ['service', 'infra']

default_infra_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" }
    },
    "required": ["name", "type", "deploy", "stages", "regions"]
}
default_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp"]
}
sfsp_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "deploy_status": { "type" : "boolean" },
        "after_deploy_timestamp" : { "type" : "string" },
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "deploy_status", "after_deploy_timestamp"]
}
rollback_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "deploy_status": { "type" : "boolean" },
        "before_deploy_timestamp" : { "type" : "string" },
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "deploy_status", "before_deploy_timestamp"]
}
migrations_up_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "deploy_status": { "type" : "boolean" }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "deploy_status"]
}
migrations_down_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "deploy_status": { "type" : "boolean" },
        "after_deploy_timestamp" : { "type" : "string" },
        "migrations_up_status": { "type" : "boolean" },
    },
    "required": [
        "name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "deploy_status", "after_deploy_timestamp", "migrations_up_status"]
}

##############################################
# Setup
##############################################

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

if aws_profile or (aws_access_key_id and aws_secret_access_key):
    cloudformation_client = boto3.client('cloudformation')
    s3_client = boto3.client('s3')
else:
    logging.error(f'AWS Credentials are not configured in the environment...')
    logging.error(f'AWS_PROFILE, or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables are not set')
    sys.exit(1)

##############################################
# Helper Functions
##############################################

def read_file(file):
    with open(file, 'r') as f:
        try:
            return yaml.full_load(f)
        except yaml.YAMLError as exception:
            raise exception

def write_traits_to_file(content, file):
    with open(file, 'w') as f:
        try:
            yaml.dump(content, f, default_flow_style=False)
        except yaml.YAMLError as exception:
            raise exception

def validate_yaml(content, validation_schema):
    validationErrors = []

    v = jsonschema.Draft4Validator(validation_schema)
    for error in v.iter_errors(content):
        validationErrors.append(error)

    if validationErrors:
        logging.error('Failed schema validation for the apps\'s yaml file provided...')
        for error in validationErrors:
            print(error.message)
        #print(f'Required schema: {yaml.dump(service_yaml_schema)}')
        print(f'Required schema: {validation_schema}')
        sys.exit(1)

def load_traits_from_file(file='traits.yml', validation_schema=default_service_yaml_schema):
    content = read_file(file)
    validate_yaml(content, validation_schema)
    return content

def run_bash(command: str):
    logging.info(f'Running command: {command}')
    subprocess.run(command, shell=True, check=True)

def dump_yaml_content(data):
    for key, value in data.items():
        print(key,':',value)

def cloudformation_get_deployment_bucket(stack):
    try:
        return cloudformation_client.describe_stack_resource(
            StackName=stack,
            LogicalResourceId='ServerlessDeploymentBucket'
        )["StackResourceDetail"]["PhysicalResourceId"]
    except ClientError as e:
        logging.warning("Service's stack was not found or the service has not been deployed yet")
        logging.warning("Describe stack resource response: %s" % e)
        return

def get_timestamps(stack, app_name, stage):
    s3_bucket = cloudformation_get_deployment_bucket(stack)
    if not s3_bucket:
        return []

    folders = s3_client.list_objects(Bucket=s3_bucket, Prefix=f'serverless/{app_name}/{stage}/', Delimiter='/')
    if not folders.get('CommonPrefixes'):
        logging.warning(f'Deployment bucket exists, but no timestamps were found for app ({app_name})')
        return []
    else:
        timestamps = []
        for folder in folders.get('CommonPrefixes'):
            timestamps.append(folder.get('Prefix').split('/')[-2].split('-')[0])
        timestamps.sort()
        return timestamps

def sls_deploy(stage, region, args, chdir_path):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls deploy --stage {stage} --region {region} {args}'
    run_bash(command)
    os.chdir(cwd)

def sls_rollback(stage, region, chdir_path, timestamp):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls rollback --timestamp {timestamp} --stage {stage} --region {region}'
    run_bash(command)
    os.chdir(cwd)

def sls_migrate(stage, region, chdir_path, function, data):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls invoke --stage {stage} --region {region} --function {function} --data {data}'
    run_bash(command)
    os.chdir(cwd)

def sls_sfsp(stage, region, chdir_path):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls sfsp --stage={stage} --region={region}'
    run_bash(command)
    os.chdir(cwd)

def populate_git_traits(app, branch, commit, version, author):
    app["branch"] = branch if branch else git_branch
    app["commit"] = commit if branch else git_commit
    app["author"] = author if branch else git_author
    app["version"] = version if branch else ''
    return app


## Check functions
def check_app_type(app, type):
    if app["type"] != type or app["type"] not in allowed_app_types:
        logging.info(f'Skipping {type} ({app["name"]}) deployment...')
        logging.info(f'App type is not ({type}) or not supported! Type passed from traits: {app["type"]}')
        sys.exit(0)

def check_app_stage_region(app, stage, region):
    if stage not in app["stages"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'Stage ({stage}) is not supported for {app["type"]} ({app["name"]}). Allowed stages: {app["stages"]}')
        sys.exit(0)

    if region not in app["regions"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'Region ({region}) is not supported for {app["type"]} ({app["name"]}). Allowed regions: {app["regions"]}')
        sys.exit(0)

    pass


def run_deploy_infra_checks(app, stage, region):
    check_app_type(app, 'infra')
    check_app_stage_region(app, stage, region)

    if not app["deploy"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'"deploy" parameter is set to False in traits file.')
        sys.exit(0)

    pass

def run_rollback_infra_checks(app, stage, region):
    check_app_type(app, 'infra')
    check_app_stage_region(app, stage, region)

    if app["deploy_status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deployment status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["before_deploy_timestamp"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deployment timestamp for ({app["name"]}) is empty')
        sys.exit(0)

    pass


def run_deploy_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    if not app["deploy"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'"deploy" parameter is set to False in traits file.')
        sys.exit(0)

    pass

def run_sfsp_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    if app["sfsp"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'Service ({app["name"]}) has no "sfsp"')
        sys.exit(0)

    if app["deploy_status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'Deployment status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["after_deploy_timestamp"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'After deploy timestamp is empty in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    pass

def run_rollback_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    if app["deploy_status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deployment status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["before_deploy_timestamp"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deployment timestamp for ({app["name"]}) is empty')
        sys.exit(0)

    pass


def run_migrations_up_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    # Check if app has migrations
    if app["migrations"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations up...')
        logging.info(f'{app["type"]} ({app["name"]}) has no migrations')
        sys.exit(0)

    # Check if deploy_status is True
    if app["deploy_status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations up...')
        logging.info(f'Deployment status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    pass

def run_migrations_down_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    # Check if service has migrations and if they were run
    if app["migrations"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations down...')
        logging.info(f'{app["type"]} ({app["name"]}) has no migrations')
        sys.exit(0)

    # ... and service migrations_up_status is True
    if app["migrations_up_status"] == False:
        logging.info(f'Skipping service ({app["name"]}) migrations down...')
        logging.info(f'{app["type"]} ({app["name"]}) migrations up was run but failed')
        sys.exit(0)

    # Check if deploy_status is True
    if app["deploy_status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations down...')
        logging.info(f'Deployment status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    # ... and service has a after_deployment_timestamp
    if app["after_deploy_timestamp"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations down...')
        logging.info(f'After deploy timestamp is empty in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    pass



##############################################
# Commands
##############################################

@click.group(chain=True)
@click.version_option()
def cli():
    pass

@cli.command("deploy-infra")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-a', '--args', type=str, default='', help='Additional sls arguments passed to the sls deploy command')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls deploy')
@click.option('--branch', type=str, default=None, help='Git branch')
@click.option('--commit', type=str, default=None, help='Git commit')
@click.option('--version', type=str, default=None, help='Version')
@click.option('--author', type=str, default=None, help='Git commit author')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def deploy_infra_cmd(stage, region, args, app_dir, branch, commit, version, author, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, default_infra_yaml_schema)
    service = populate_git_traits(service, branch, commit, version, author)
    service["nx_app_name"] = service["type"] + "-" + service["name"]
    service["cloudformation_stack"] = service["name"] + "-" + stage
    service["before_deploy_timestamp"] = ''
    service["after_deploy_timestamp"] = ''
    service["deploy_run"] = False
    service["deploy_status"] = False
    write_traits_to_file(service, traits_output_file)

    run_deploy_infra_checks(service, stage, region)

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'Last deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["before_deploy_timestamp"] = timestamps[0]
        write_traits_to_file(service, traits_output_file)

    logging.info(f'Deploying infra ({service["name"]}) on ({stage}) in ({region})...')
    service["deploy_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_deploy(stage, region, args, app_dir)

    service["deploy_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'New deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["after_deploy_timestamp"] = timestamps[0]
        write_traits_to_file(service, traits_output_file)

@cli.command("rollback-infra")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-t', '--timestamp', type=str, default=None, help='Serverless timestamp')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def rollback_infra_cmd(stage, region, timestamp, app_dir, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, rollback_service_yaml_schema)
    service["cloudformation_stack"] = service["name"] + "-" + stage
    service["rollback_status"] = False
    service["rollback_run"] = False
    service["rollback_timestamp"] = ''
    service["before_deploy_timestamp"] = str(timestamp) if timestamp else service["before_deploy_timestamp"]
    write_traits_to_file(service, traits_output_file)

    run_rollback_infra_checks(service, stage, region)

    logging.info(f'Rolling back infra ({service["name"]}) to timestamp ({service["before_deploy_timestamp"]})...')
    service["rollback_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_rollback(stage, region, app_dir, timestamp)

    service["rollback_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'Rollback deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["rollback_timestamp"] = timestamps[0]
        write_traits_to_file(service, traits_output_file)


@cli.command("deploy-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-a', '--args', type=str, default='', help='Additional sls arguments passed to the sls deploy command')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls deploy')
@click.option('--branch', type=str, default=None, help='Git branch')
@click.option('--commit', type=str, default=None, help='Git commit')
@click.option('--version', type=str, default=None, help='Version')
@click.option('--author', type=str, default=None, help='Git commit author')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def deploy_service_cmd(stage, region, args, app_dir, branch, commit, version, author, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, default_service_yaml_schema)
    service = populate_git_traits(service, branch, commit, version, author)
    service["nx_app_name"] = service["type"] + "-" + service["name"]
    service["cloudformation_stack"] = service["name"] + "-" + stage
    service["before_deploy_timestamp"] = ''
    service["after_deploy_timestamp"] = ''
    service["deploy_status"] = False
    service["deploy_run"] = False
    write_traits_to_file(service, traits_output_file)

    run_deploy_service_checks(service, stage, region)

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'Last deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["before_deploy_timestamp"] = timestamps[0]
        write_traits_to_file(service, traits_output_file)

    logging.info(f'Deploying service ({service["name"]}) on ({stage}) in ({region})...')
    service["deploy_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_deploy(stage, region, args, app_dir)

    service["deploy_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'New deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["after_deploy_timestamp"] = timestamps[0]
        write_traits_to_file(service, traits_output_file)


@cli.command("sfsp")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def sfsp_cmd(stage, region, app_dir, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, sfsp_yaml_schema)
    service["sfsp_status"] = False
    service["sfsp_run"] = False
    service["sfsp_timestamp"] = ''
    write_traits_to_file(service, traits_output_file)

    run_sfsp_checks(service, stage, region)

    logging.info(f'Running sfsp for service ({service["name"]})...')
    service["sfsp_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_sfsp(stage, region, app_dir)

    service["sfsp_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamp = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    logging.info(f'Sfsp timestamp: {str(timestamp)}')
    service["sfsp_timestamp"] = str(timestamp)
    write_traits_to_file(service, traits_output_file)


@cli.command("rollback-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-t', '--timestamp', type=str, default=None, help='Serverless timestamp')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def rollback_service_cmd(stage, region, timestamp, app_dir, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, rollback_service_yaml_schema)
    service["cloudformation_stack"] = service["name"] + "-" + stage
    service["rollback_status"] = False
    service["rollback_run"] = False
    service["rollback_timestamp"] = ''
    service["before_deploy_timestamp"] = str(timestamp) if timestamp else service["before_deploy_timestamp"]
    write_traits_to_file(service, traits_output_file)

    run_rollback_service_checks(service, stage, region)

    logging.info(f'Rolling back service ({service["name"]}) to timestamp ({service["before_deploy_timestamp"]})...')
    service["rollback_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_rollback(stage, region, app_dir, timestamp)

    service["rollback_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'Rollback deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["rollback_timestamp"] = timestamps[0]
        write_traits_to_file(service, traits_output_file)


@cli.command("migrations-up-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-d', '--data', type=str, default='{}', help='Migration data param passed to "up" function')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def migrations_up_service_cmd(stage, region, data, app_dir, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, migrations_up_service_yaml_schema)
    service["migrations_up_status"] = False
    service["migrations_up_run"] = False
    service["migrations_up_timestamp"] = ''
    write_traits_to_file(service, traits_output_file)

    run_migrations_up_service_checks(service, stage, region)

    logging.info(f'Running migrations UP for service ({service["name"]})...')
    service["migrations_up_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_migrate(stage, region, app_dir, "up", data)

    service["migrations_up_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamp = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    logging.info(f'Migrations up timestamp: {str(timestamp)}')
    service["migrations_up_timestamp"] = str(timestamp)
    write_traits_to_file(service, traits_output_file)


@cli.command("migrations-down-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-d', '--data', type=str, default='{}', help='Migration data param passed to "up" function')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def migrations_down_service_cmd(stage, region, data, app_dir, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file, migrations_down_service_yaml_schema)
    service["migrations_down_status"] = False
    service["migrations_down_run"] = False
    service["migrations_down_timestamp"] = ''
    write_traits_to_file(service, traits_output_file)

    run_migrations_down_service_checks(service, stage, region)

    logging.info(f'Running migrations DOWN for service ({service["name"]})...')
    service["migrations_down_run"] = True
    write_traits_to_file(service, traits_output_file)

    sls_migrate(stage, region, app_dir, "down", data)

    service["migrations_down_status"] = True
    write_traits_to_file(service, traits_output_file)

    timestamp = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    logging.info(f'Migrations down timestamp: {str(timestamp)}')
    service["migrations_down_timestamp"] = str(timestamp)
    write_traits_to_file(service, traits_output_file)



if __name__ == "__main__":
    cli()
