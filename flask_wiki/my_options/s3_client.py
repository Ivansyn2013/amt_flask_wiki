import boto3
from botocore.client import Config
from dotenv import load_dotenv
import os

load_dotenv('../../.env')
load_dotenv()
BUCKET = os.getenv("BUCKET_NAME")
def create_client():
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('ENDPOINT'),
        region_name=os.getenv('REGION_NAME'),
        aws_access_key_id=os.getenv('ACCESS_KEY'),
        aws_secret_access_key=os.getenv('SECRET_KEY'),
        config=Config(s3={'addressing_style': 'path'})
    )

    return s3
