import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

from users_crm.config import settings
from users_crm.schemas.users import UserSchemaAddDb

DEFAULT_USER = UserSchemaAddDb(
    email='admin@example.com',
    password='admin123',
    first_name='Admin',
    last_name='User',
    role='admin',
    is_active=True,
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def initialize_default_user():
    client = AsyncIOMotorClient(str(settings.MONGO_URI))
    try:
        db = client[settings.MONGO_DATABASE_NAME]
        users_collection = db[settings.MONGO_USER_COLLECTION_NAME]

        existing_user = await users_collection.find_one({'email': DEFAULT_USER.email})
        if not existing_user:
            user_data = DEFAULT_USER.model_dump()
            user_data['password'] = pwd_context.hash(user_data['password'])
            await users_collection.insert_one(user_data)
    finally:
        client.close()


if __name__ == '__main__':
    asyncio.run(initialize_default_user())
