import click
import logging
import sys,os
import yaml
import jsonschema
import subprocess
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

aws_profile = os.getenv('AWS_PROFILE')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

git_branch = os.getenv('GITHUB_REF_NAME', '')
git_commit = os.getenv('GITHUB_SHA', '')
git_author = os.getenv('GITHUB_ACTOR', '')

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : {
            "type" : "string"
        },
        "type" : {
            "type" : "string"
        },
        "deploy" : {
            "type" : "boolean"
        },
        "stages" : {
            "type" : "array"
        },
        "regions" : {
            "type" : "array"
        },
    },
    "required": ["name", "type", "deploy", "stages", "regions"]
}

if aws_profile or (aws_access_key_id and aws_secret_access_key):
    cloudformation_client = boto3.client('cloudformation')
    s3_client = boto3.client('s3')
else:
    logging.error(f'AWS_PROFILE, or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables are not set')
    sys.exit(1)



def read_file(file):
    if not os.path.isfile(file):
        logging.error(f'Yaml file ({file}) does not exist!')
        sys.exit(1)
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

def validate_yaml(content):
    validationErrors = []

    v = jsonschema.Draft4Validator(service_yaml_schema)
    for error in v.iter_errors(content):
        validationErrors.append(error)

    if validationErrors:
        logging.error('Failed schema validation for the service\'s yaml file provided...')
        for error in validationErrors:
            print(error.message)
        #print(f'Required schema: {yaml.dump(service_yaml_schema)}')
        print(f'Required schema: {service_yaml_schema}')
        sys.exit(1)

def load_traits_from_file(file='traits.yml'):
    content = read_file(file)
    validate_yaml(content)
    return content

def run_bash(command: str):
    logging.info(f'Running command: {command}')
    subprocess.run(command, shell=True, check=True)

def dump_yaml_content(data):
    for key, value in data.items():
        print(key,':',value)

def run_service_deployment_checks(service, stage, region):
    if not service["deploy"]:
        logging.info(f'Skipping ({service["name"]}) deployment...')
        logging.info(f'"deploy" parameter is set to False in traits file.')
        sys.exit(0)

    if stage not in service["stages"]:
        logging.info(f'Skipping ({service["name"]}) deployment...')
        logging.info(f'Stage ({stage}) is not supported for service ({service["name"]}). Allowed stages: {service["stages"]}')
        sys.exit(0)

    if region not in service["regions"]:
        logging.info(f'Skipping ({service["name"]}) deployment...')
        logging.info(f'Region ({region}) is not supported for service ({service["name"]}). Allowed regions: {service["regions"]}')
        sys.exit(0)

    pass

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

def get_timestamps(stack, service_name, stage):
    s3_bucket = cloudformation_get_deployment_bucket(stack)
    if not s3_bucket:
        return []

    folders = s3_client.list_objects(Bucket=s3_bucket, Prefix=f'serverless/{service_name}/{stage}/', Delimiter='/')
    if not folders.get('CommonPrefixes'):
        logging.warning(f'Deployment bucket exists, but no timestamps were found for service ({service_name})')
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

def populate_git_traits(service, branch, commit, version, author):
    service["branch"] = branch if branch else git_branch
    service["commit"] = commit if branch else git_commit
    service["author"] = author if branch else git_author
    service["version"] = version if branch else ''
    return service

@click.group(chain=True)
def cli():
    pass



@cli.command("deploy-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-a', '--args', type=str, default='', help='Additional sls arguments passed to the sls deploy command')
@click.option('--service-dir', type=str, default='.', help='Service directory where to run sls deploy')
@click.option('--branch', type=str, default=None, help='Git branch')
@click.option('--commit', type=str, default=None, help='Git commit')
@click.option('--version', type=str, default=None, help='Version')
@click.option('--author', type=str, default=None, help='Git commit author')
@click.option('--traits-input-file', type=str, default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=str, default='traits.yml', help='Updated traits file. Default (traits.yml)')
def deploy_service_cmd(stage, region, args, service_dir, branch, commit, version, author, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file)
    service = populate_git_traits(service, branch, commit, version, author)
    service["nx_app_name"] = service["type"] + "-" + service["name"]
    service["cloudformation_stack"] = service["name"] + "-" + stage

    run_service_deployment_checks(service, stage, region)

    service["before_deploy_timestamp"] = ''
    service["after_deploy_timestamp"] = ''
    service["deployment_status"] = False

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'Last deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["before_deploy_timestamp"] = int(timestamps[0])

    sls_deploy(stage, region, args, service_dir)
    service["deployment_status"] = True

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'New deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["after_deploy_timestamp"] = int(timestamps[0])

    write_traits_to_file(service, traits_output_file)

@cli.command("rollback-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-t', '--timestamp', type=str, default=None, help='Serverless timestamp')
@click.option('--service-dir', type=str, default='.', help='Service directory where to run sls rollback')
@click.option('--traits-input-file', type=str, default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=str, default='traits.yml', help='Updated traits file. Default (traits.yml)')
def rollback_service_cmd(stage, region, timestamp, service_dir, traits_input_file, traits_output_file):
    service = load_traits_from_file(traits_input_file)
    service["cloudformation_stack"] = service["name"] + "-" + stage

    if timestamp or "before_deploy_timestamp" in service:
        timestamp = timestamp if timestamp else service["before_deploy_timestamp"]

    if not "deployment_status" in service or service["deployment_status"] == False:
        logging.warning(f'Deployment status is "FALSE" or not found in ({service["name"]}) traits')
        logging.warning(f'Skipping rollback...')
        sys.exit(0)

    if timestamp == '':
        logging.warning(f'Deployment timestamp for ({service["name"]}) is empty')
        logging.warning(f'Skipping rollback...')
        sys.exit(0)

    logging.info(f'Rolling back service ({service["name"]}) to timestamp ({timestamp})...')
    sls_rollback(stage, region, service_dir, timestamp)

    service["rollback_status"] = True

    timestamps = get_timestamps(service["cloudformation_stack"], service["name"], stage)
    if timestamps:
        logging.info(f'Rollback deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        service["rollback_timestamp"] = int(timestamps[0])

    write_traits_to_file(service, traits_output_file)


@cli.command('deploy-ui')
@click.option('--bucket', required=True, type=str, help='S3 Bucket name where files will be deployed')
@click.option('--version', required=True, type=str, help='UI version for creating backup folders in S3')
@click.option('--distribution-id', required=True, type=str, help='CloudFront Distribution ID for cache invalidation')
@click.option('--distribution-invalidation-path', type=str, default='/*', help='CloudFront Distribution path to invalidate cache')
def deploy_ui_cmd(bucket, version, distribution_id, distribution_invalidation_path):
    print(f"aws cloudfront create-invalidation --distribution-id {distribution_id} --paths \"{distribution_invalidation_path}\"")

if __name__ == "__main__":
    cli()
