# from pymongo.mongo_client import MongoClient
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    _instance = None
    _collection = None

    def __new__(cls):
        if cls._instance is None:

            # Cache the instance, so that we don't have to connect again in signle run
            cls._instance = super().__new__(cls)
            cls._instance.client = AsyncIOMotorClient(settings.MONGO_DB_URL)
            try:
                cls._instance.client.admin.command("ping")
                print("successfully connected to MongoDB!")
                cls._instance.db = cls._instance.client[settings.DATABASE]
            except Exception as e:
                raise e
            return cls._instance
        else:
            return cls._instance

    def load_collection(self):
        """
        Cache the collection instance
        """
        if self._collection is None:
            self._collection = self.db[settings.COLLECTION]
        return self._collection
