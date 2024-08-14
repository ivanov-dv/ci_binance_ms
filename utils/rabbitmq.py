import asyncio
import logging

import aio_pika
from aio_pika.exceptions import ConnectionClosed


class RabbitMq:
    def __init__(self, user, password, queue_name, host='localhost', port=5672):
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.url = f'amqp://{self.host}:{port}/'
        self.connection = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url, login=self.user, password=self.password)

    async def send_message(self, message):
        self.connection = await aio_pika.connect_robust(self.url, login=self.user, password=self.password)
        try:
            async with self.connection:
                channel = await self.connection.channel()
                await channel.declare_queue(self.queue_name, durable=True)
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=message.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                    ),
                    routing_key=self.queue_name,
                )
        except ConnectionClosed:
            await asyncio.sleep(1)
            logging.error("Connection closed by broker, attempting to reconnect")
            await self.connect()
            await self.send_message(message)

