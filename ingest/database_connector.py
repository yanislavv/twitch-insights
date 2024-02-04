from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnector:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = None
        self.engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db}")

    def connect(self):
        try:
            self.connection = sessionmaker(bind=self.engine)
            if self.connection().is_active:
                print(f"Connected to {self.connection().bind}")
        except Exception as e:
            print(e)


db_connector = DatabaseConnector('172.18.0.3', 'root', 'admin', 'twitch_insights') # mysql docker container IP used
db_connector.connect()
