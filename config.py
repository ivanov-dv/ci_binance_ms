import logging
import os
import sys
from dotenv import load_dotenv

import utils.assist as assist


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


'''
LOGGING
'''
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


'''
PROXIES
'''
PROXIES = assist.get_proxies()


'''
RabbitMQ
'''
# RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
# RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
# RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
# RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
# RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')
#
#
# '''
# PostgreSQL
# '''
# POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
# POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
# POSTGRESQL_HOST = 'localhost'
# POSTGRESQL_PORT = 5432
# POSTGRESQL_DATABASE = 'crypto_informer'


'''
Binance API
'''
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
TIME_PERIODS = {'5m', '30m', '1h', '4h', '8h', '12h', '1d', '1w', '1M'}
INTERVAL_FOR_PRICE_REQUEST = '1m'
LIMIT_FOR_PRICE_REQUEST = 3
TRY_GET_RESPONSE = 3
TIMEOUT_BETWEEN_RESPONSE = 1
THREAD_INTERVAL_BETWEEN_RESPONSE = 0.05
WEIGHT_GET_TICKER = 2
WEIGHT_GET_KLINES = 2
WEIGHT_REQUEST_KLINE = WEIGHT_GET_KLINES * LIMIT_FOR_PRICE_REQUEST
