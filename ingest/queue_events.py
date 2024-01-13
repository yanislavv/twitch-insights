import time
import json

from services.aws import AWSServices as aws
from configs.variables import AppConfig
from ingest.writer import DatabaseWriter
from table_manager import raw_messages_table


def get_s3_object(queue_event):
    messages = queue_event.get('Messages', [])
    for message in messages:
        message_id = message['ReceiptHandle']
        message_body = json.loads(message['Body'])['Records']
        for message_key in message_body:
            key = message_key['s3']['object']['key']
            if key:
                yield key, message_id


def main():

    while True:
        response = aws.get_message(AppConfig.QUEUE_URL.value)
        print(response)

        for key, message_id in get_s3_object(response):
            print(key, message_id)
            records = aws.read_s3(AppConfig.BUCKET_STAGING.value, key)
            for record in json.loads(records).values():
                # TODO: maki it generic, get configurationId from message and map it corresponding schema file
                if DatabaseWriter.validate_schema('schemas/raw_messages.json', record[0], key):
                    record = DatabaseWriter.add_partitions(record[0])
                    print(record)
                    DatabaseWriter.write_to_db(raw_messages_table, record)

            aws.delete_message(AppConfig.QUEUE_URL.value, message_id)

        time.sleep(10)


if __name__ == '__main__':
    main()
