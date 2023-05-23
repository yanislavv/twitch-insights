import boto3
import s3transfer.upload


class AWSServices:

    region = 'eu-central-1'
    s3_client = boto3.client('s3')

    @classmethod
    def upload_s3(cls, file, bucket, s3_key):
        return cls.s3_client.upload_file(file, bucket, s3_key)
