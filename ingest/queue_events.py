import time
import json

from services.aws import AWSServices as aws
from configs.variables import AppConfig
from ingest.writer import DatabaseWriter
from table_manager import raw_messages_table


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
        print(response)
        keys = get_s3_object(response)
        for key in keys:
            records = aws.read_s3(AppConfig.BUCKET_STAGING.value, key)
            for record in json.loads(records).values():
                if DatabaseWriter.validate_schema('schemas/raw_messages.json', record[0], key):
                    record = DatabaseWriter.add_partitions(record[0])
                    print(record)
                    DatabaseWriter.write_to_db(raw_messages_table, record)
        time.sleep(10)


if __name__ == '__main__':
    main()
