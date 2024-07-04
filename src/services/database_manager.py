from sqlalchemy import create_engine, text
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

import os

class DatabaseManager:
    def __init__(self, db_engine: str) -> None:
        self.conn = create_engine(db_engine).connect()


db_engine = config["DB_URL"]
dbInstance = DatabaseManager(db_engine=db_engine)