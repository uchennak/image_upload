import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
import sys


class ParameterStoreError(Exception):
    """Raised when Parameter Store is unavailable"""
    pass


def get_parameter(parameter_name, required=True):
    try:
        ssm = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        value = response['Parameter']['Value']
        return value

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ParameterNotFound':
            error_msg = f"Parameter '{parameter_name}' not found in Parameter Store"
        else:
            error_msg = f"AWS Error accessing '{parameter_name}': {error_code}"

        if required:
            print(f"ERROR: {error_msg}", file=sys.stderr)
            raise ParameterStoreError(error_msg)
        else:
            print(f"Warning: {error_msg}")
            return None

    except NoCredentialsError:
        error_msg = "AWS credentials not configured. Run 'aws configure' or set IAM role."
        print(f"ERROR: {error_msg}", file=sys.stderr)
        if required:
            raise ParameterStoreError(error_msg)
        return None

    except Exception as e:
        error_msg = f"Unexpected error fetching '{parameter_name}': {str(e)}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        if required:
            raise ParameterStoreError(error_msg)
        return None
