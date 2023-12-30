from sqlalchemy import text, insert
from database_connector import DatabaseConnector


class DatabaseWriter:
    def __init__(self, database_connector):
        self.database_connector = database_connector

    def write_to_db(self, table, data):
        try:
            if not self.database_connector.connection:
                self.database_connector.connect()

            with self.database_connector.connection() as session:
                result = session.execute(insert(table).values(data))
                response = result.fetchall()
                print(response)

        except Exception as e:
            print(e)


eng = DatabaseConnector('localhost', 'root', 'admin', 'twitch_insights')

database = DatabaseWriter(eng)
database.write_to_db('tete', 'rerer')

