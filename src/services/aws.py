import boto3
from src import ExtractVar


class AWSServices:

    region = 'eu-central-1'
    s3_client = boto3.client('s3')
    sqs = boto3.client('sqs')

    @classmethod
    def upload_s3(cls, file, bucket, s3_key):
        return cls.s3_client.upload_fileobj(file, bucket, s3_key)
    
    @classmethod
    def get_message(cls):
        response = cls.sqs.receive_message(
            QueueUrl=ExtractVar.QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
            )
        return response
