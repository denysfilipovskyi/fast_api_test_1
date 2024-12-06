from users_crm.config import settings
from users_crm.db.mongo_motor_client import MongoMotorDBClient
from users_crm.repositories.abstract.nosql import AbstractNoSqlRepository


class MongoMotorRepository(AbstractNoSqlRepository):
    collection_name = None

    def __init__(self):
        self.db_client = MongoMotorDBClient(
            str(settings.MONGO_URI), settings.MONGO_DATABASE_NAME)

    async def add_one(self, data: dict[str, str | bool]):
        async with self.db_client as database:
            collection = database.get_collection(self.collection_name)
            new_row = await collection.insert_one(data)
            return new_row.inserted_id

    async def update_one(self, id, data: dict[str, str | bool]):
        async with self.db_client as database:
            collection = database.get_collection(self.collection_name)
            await collection.find_one_and_update(
                {'_id': id},
                {'$set': data},
            )
            return await collection.find_one({'_id': id})

    async def find_one(self, filters: dict[str, str | bool]):
        async with self.db_client as database:
            collection = database.get_collection(self.collection_name)
            return await collection.find_one(filters)

    async def delete(self, filters: dict[str, str | bool] = {}):
        async with self.db_client as database:
            collection = database.get_collection(self.collection_name)
            result = await collection.delete_many(filters)
            return result.deleted_count
