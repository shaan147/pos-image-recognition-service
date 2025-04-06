from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from .settings import settings
import time

class DatabaseConnection:
    _instance = None
    _max_retries = 3
    _retry_delay = 2  # seconds

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        retries = 0
        while retries < self._max_retries:
            try:
                self.client = MongoClient(
                    settings.MONGODB_URI,
                    serverSelectionTimeoutMS=5000,  # 5 second timeout
                    connectTimeoutMS=5000,
                    maxPoolSize=10  # Connection pooling
                )
                # Test connection
                self.client.admin.command('ping')
                self.database = self.client[settings.DATABASE_NAME]
                return
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                retries += 1
                if retries >= self._max_retries:
                    raise ConnectionError(f"Failed to connect to MongoDB after {self._max_retries} attempts: {str(e)}")
                print(f"MongoDB connection attempt {retries} failed. Retrying in {self._retry_delay} seconds...")
                time.sleep(self._retry_delay)

    def get_database(self):
        return self.database

    def get_product_collection(self):
        return self.database['products']
        
    def close_connection(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()
            print("MongoDB connection closed")

db_connection = DatabaseConnection()

# Register a shutdown handler to close connections
import atexit
atexit.register(db_connection.close_connection)