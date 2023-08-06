import os
import json
import base64
from typing import Literal, Dict
import boto3
from botocore.exceptions import ClientError


def get_secret(
    secret_name: str,
    region_name: str,
    environment: Literal['DEV', 'STG', 'PROD']
) -> Dict:
    # Create a Secrets Manager client
    session = boto3.session.Session(
        aws_access_key_id=os.environ.get(f'{environment}_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get(f'{environment}_AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.environ.get(f'{environment}_AWS_SESSION_TOKEN')
    )
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(secret)
