import time
import json

from services.aws import AWSServices as aws
from configs.variables import AppConfig
from ingest.table_manager import TableManager


def get_s3_object(queue_event):
    messages = queue_event.get('Messages', [])
    for message in messages:
        message_body = json.loads(message['Body'])['Records']
        for message_key in message_body:
            key = message_key['s3']['object']['key']
            if key:
                yield key


def main():
    while True:

        response = aws.get_message(AppConfig.QUEUE_URL.value)
        keys = get_s3_object(response)
        for key in keys:
            records = aws.read_s3(AppConfig.BUCKET_STAGING.value, key)
            for record in json.loads(records).values():
                if TableManager.validate_schema('schemas/raw_messages.json', record[0], key):
                    #insert to db
                    print('here')
        time.sleep(10)


if __name__ == '__main__':
    main()
