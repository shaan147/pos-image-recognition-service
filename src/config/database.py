from pymongo import MongoClient
from .settings import settings

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(settings.MONGODB_URI)
            cls._instance.database = cls._instance.client[settings.DATABASE_NAME]
        return cls._instance

    def get_database(self):
        return self.database

    def get_product_collection(self):
        return self.database['products']

db_connection = DatabaseConnection()