from users_crm.config import settings
from users_crm.repositories.mongo_motor import MongoMotorRepository


class UserRepository(MongoMotorRepository):
    collection_name = settings.MONGO_USER_COLLECTION_NAME
