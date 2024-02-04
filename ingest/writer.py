import json

from sqlalchemy import text, insert
from ingest.database_connector import db_connector
from datetime import datetime


class DatabaseWriter:
    database_connector = db_connector

    @classmethod
    def write_to_db(cls, table, data):
        try:
            if not cls.database_connector.connection:
                cls.database_connector.connect()

            with cls.database_connector.connection() as session:
                result = session.execute(table.insert().values(data))
                session.commit()

        except Exception as e:
            print(e)

    @staticmethod
    def add_partitions(record):
        record_date = datetime.fromtimestamp(float(record['tmi-sent-ts']) / 1000)
        record.update({'year': record_date.strftime('%Y'), 'month': record_date.strftime('%m'), 'day': record_date.strftime('%d')})
        return record

    @staticmethod
    def validate_schema(schema_file, record, file_key):
        with open(schema_file, 'r') as file:
            schema = json.load(file)

        delete_keys = []
        for col, val in record.items():
            if any(schema_col for schema_col in schema if col == schema_col):
                if not isinstance(val, eval(schema[col]['type'])):
                    # TODO: write invalid record to log file
                    break
            else:
                delete_keys.append(col)
        if delete_keys:
            for key in delete_keys:
                del record[key]
        missing_keys = set(schema.keys()).difference(set(record.keys()))
        if missing_keys:
            print(f"Following keys are missing from the schema --> {', '.join(missing_keys)}:\n"
                  f"File -> {file_key}\nRecord -> {record}")
            return False
        return True
