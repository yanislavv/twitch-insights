import json

from sqlalchemy import Table, MetaData, Column, String, inspect
from database_connector import DatabaseConnector


raw_massages_columns = [
    Column('badge-info', String(length=255)),
    Column('badges', String(length=255)),
    Column('client-nonce', String(length=255)),
    Column('color', String(length=255)),
    Column('display-name', String(length=255)),
    Column('emotes', String(length=255)),
    Column('first-msg', String(length=255)),
    Column('flags', String(length=255)),
    Column('id', String(length=255)),
    Column('mod', String(length=255)),
    Column('returning-chatter', String(length=255)),
    Column('room-id', String(length=255)),
    Column('subscriber', String(length=255)),
    Column('turbo', String(length=255)),
    Column('user-id', String(length=255)),
    Column('user-type', String(length=255)),
    Column('year', String(length=255)),
    Column('month', String(length=255)),
    Column('day', String(length=255)),
]


class TableManager:
    def __init__(self, database_connector, table_name: str, columns: list):
        self.database_connector = database_connector
        self.metadata = MetaData(schema=self.database_connector.db)
        self.table = Table(table_name, self.metadata, *columns)
        self.inspector = inspect(self.database_connector.engine)

    def create_table(self):
        self.table.create(self.database_connector.engine)

    def drop_table(self):
        self.table.drop(self.database_connector.engine)

    def get_schema(self):
        return self.inspector.get_columns(self.table.name)

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


# eng = DatabaseConnector('localhost', 'root', 'admin', 'twitch_insights')
#
# mng = TableManager(eng, 'raw_messages', raw_massages_columns)
# print(mng.create_table())