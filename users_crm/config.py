from pydantic import AmqpDsn, MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: MongoDsn = 'mongodb://mongodb:27017'
    MONGO_DATABASE_NAME: str = 'users_crm'
    MONGO_USER_COLLECTION_NAME: str = 'users'
    RABBIT_MQ_URL: AmqpDsn = 'amqp://guest:guest@rabbitmq:5672/'
    SECRET_KEY: str = 'your-secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
