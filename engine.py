import pika

import config as cfg


from binance import Client

from utils.db import PostgresDB
from utils.repositories import RequestRepository
from utils.service import Monitoring

'''
RabbitMQ
'''
# credentials = pika.PlainCredentials(
#     username=cfg.RABBITMQ_USERNAME,
#     password=cfg.RABBITMQ_PASSWORD,
#     erase_on_connect=True)
# parameters = pika.ConnectionParameters(
#     host=cfg.RABBITMQ_HOST,
#     port=cfg.RABBITMQ_PORT,
#     virtual_host=cfg.RABBITMQ_VHOST,
#     credentials=credentials)
# connection_rabbitmq = pika.BlockingConnection(parameters)


'''
PostgreSQL
'''
# connection_postgres = PostgresDB(
#     username=cfg.POSTGRESQL_USERNAME,
#     password=cfg.POSTGRESQL_PASSWORD,
#     host=cfg.POSTGRESQL_HOST,
#     port=cfg.POSTGRESQL_PORT,
#     database=cfg.POSTGRESQL_DATABASE
# )


'''
Binance API
'''
binance_bot = Client(api_key=cfg.BINANCE_API_KEY, api_secret=cfg.BINANCE_API_SECRET)
monitoring = Monitoring(binance_bot)


'''
Repositories
'''
req_repo = RequestRepository('db')
