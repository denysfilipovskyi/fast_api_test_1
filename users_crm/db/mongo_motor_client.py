from motor.motor_asyncio import AsyncIOMotorClient


class MongoMotorDBClient:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.database = None

    async def __aenter__(self):
        self.client = AsyncIOMotorClient(self.uri)
        self.database = self.client[self.db_name]
        return self.database

    async def __aexit__(self, *_):
        if self.client:
            self.client.close()
