from typing import Final

USERS_RMQ_QUEUE_NAME: Final = 'user_created_queue'
USERS_RMQ_EXCHANGE_NAME: Final = 'amq.topic'
USERS_RMQ_GAM_ROUTING_KEY: Final = 'crm.user.created'
