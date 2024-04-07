import boto3
from botocore.client import Config
from dotenv import load_dotenv
import os

load_dotenv('../../.env')
load_dotenv()
BUCKET = os.getenv("BUCKET_NAME")

def get_obj_from_bucket(s3):
    '''вернет список объектов из бакета , но если их больше 1000 нужен пагинатор'''
    return [folder_name['Key'] for folder_name in s3.list_objects(Bucket=BUCKET)['Contents']]

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

def check_folder_exists(s3, folder_name):
    '''проверяет есть ли такая папка и создает если нет'''
    if folder_name not in get_obj_from_bucket(s3):
        s3.put_object(Bucket=BUCKET, Key=folder_name)
        print('folder {} created'.format(folder_name))
        return False
    return True

def create_folder(s3, folder_name):
    '''
    Создает объект как папку. Папка должна кончатьcя на /
    :param s3:
    :param folder_name:
    :return:
    '''
    try:
        s3.put_object(Bucket=BUCKET, Key=f'{folder_name}/')
        return folder_name
    except Exception as e:
        print(f'failed to create folder {folder_name} \n {e}')