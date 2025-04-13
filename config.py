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
RABBITMQ_USER = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
RABBITMQ_QUEUE = 'ci_to_telegram'

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
INTERVAL_BETWEEN_RESPONSE = 0.05
WEIGHT_PRICE = 2
CUMULATIVE_WEIGHT_THROTTLING_MONITORING = 4500
CUMULATIVE_WEIGHT_THROTTLING_PRICE = 800
TIMEOUT_CUMULATIVE_WEIGHT = 1

'''
HOSTS
'''
REPO_HOST = os.getenv('REPO_HOST')

'''
SENTRY
'''
SENTRY_DSN = os.getenv('SENTRY_DSN')
