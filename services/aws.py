import boto3
from botocore.exceptions import ClientError


class AWSServices:

    region = 'eu-central-1'
    s3_client = boto3.client('s3', region)
    sqs = boto3.client('sqs', region)

    @classmethod
    def upload_s3(cls, file, bucket, s3_key):
        return cls.s3_client.upload_fileobj(file, bucket, s3_key)

    @classmethod
    def read_s3(cls, bucket, key):
        # TODO try exception
        response = cls.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode("utf-8")
    
    @classmethod
    def get_message(cls, queue_url):
        response = cls.sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1
            )
        return response

    @classmethod
    def delete_message(cls, queue_url, message_id):
        try:
            response = cls.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message_id
            )
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ReceiptHandleIsInvalid':
                print(f'Provided message_id is invalid: {message_id}')
            else:
                print(e.response)
