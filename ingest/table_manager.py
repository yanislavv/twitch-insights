from sqlalchemy import Table, MetaData, Column, String, inspect
from database_connector import DatabaseConnector

metadata = MetaData()
raw_massages_columns = [
    Column('@badge-info', String(length=255)),
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
    Column('tmi-sent-ts', String(length=255)),
    Column('turbo', String(length=255)),
    Column('user-id', String(length=255)),
    Column('user-type', String(length=255)),
    Column('year', String(length=255)),
    Column('month', String(length=255)),
    Column('day', String(length=255)),
]
raw_messages_table = Table('raw_messages_new', metadata, *raw_massages_columns)


class TableManager:
    def __init__(self, database_connector, table: Table):
        self.database_connector = database_connector
        self.table = table
        self.inspector = inspect(self.database_connector.engine)

    def create_table(self):
        self.table.create(self.database_connector.engine)

    def drop_table(self):
        self.table.drop(self.database_connector.engine)

    def get_schema(self):
        return self.inspector.get_columns(self.table.name)


# eng = DatabaseConnector('localhost', 'root', 'admin', 'twitch_insights')
#
# mng = TableManager(eng, raw_messages_table)
# print(mng.create_table())
