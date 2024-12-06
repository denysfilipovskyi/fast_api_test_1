import json

import aio_pika

from users_crm.config import settings
from users_crm.constance import USERS_RMQ_EXCHANGE_NAME


class RabbitMQRepository():

    async def _connect(self):
        return await aio_pika.connect_robust(str(settings.RABBIT_MQ_URL))

    async def publish_message(
            self, msg: json, routing_key: str, queue_name: str) -> None:
        connection = await self._connect()
        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange(
                USERS_RMQ_EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True)

            queue = await channel.declare_queue(
                queue_name, durable=True
            )

            await queue.bind(exchange, routing_key=routing_key)

            msg_bytes = json.dumps(msg).encode('utf-8')
            await exchange.publish(
                aio_pika.Message(body=msg_bytes),
                routing_key=routing_key
            )
