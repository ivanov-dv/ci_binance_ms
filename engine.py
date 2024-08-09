import asyncio
from pprint import pprint

import config as cfg

from binance import Client
from fastapi import FastAPI

from utils.models import RequestForServer, Price, PercentOfTime, Period, PercentOfPoint, Way, UniqueUserRequest
from utils.repositories import Repository
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
Repositories
'''
repo = Repository()

'''
Binance API
'''
binance_bot = Client(api_key=cfg.BINANCE_API_KEY, api_secret=cfg.BINANCE_API_SECRET)
monitoring = Monitoring(binance_bot, repo)

'''
FastAPI
'''
app = FastAPI()


reqs = [
    UniqueUserRequest(request_id=1, symbol='BTCUSDT', request_data=Price(target_price=10000, weight=6), way=Way.up_to),
    UniqueUserRequest(request_id=2, symbol='ETHUSDT', request_data=Price(target_price=5000, weight=6), way=Way.up_to),
    UniqueUserRequest(request_id=2, symbol='XRPUSDT', request_data=Price(target_price=200, weight=6), way=Way.up_to),
    UniqueUserRequest(request_id=2, symbol='BNBUSDT', request_data=Price(target_price=3000, weight=6), way=Way.up_to),
    UniqueUserRequest(request_id=2, symbol='GRTUSDT', request_data=Price(target_price=60000, weight=6), way=Way.up_to),
    UniqueUserRequest(request_id=2, symbol='XRPUSDT', request_data=Price(target_price=60000, weight=6), way=Way.down_to),
    UniqueUserRequest(request_id=2, symbol='IQUSDT', request_data=Price(target_price=60000, weight=6), way=Way.down_to),
    UniqueUserRequest(request_id=2, symbol='STRAXUSDT', request_data=Price(target_price=300, weight=6), way=Way.down_to),
    UniqueUserRequest(request_id=2, symbol='CYBERUSDT', request_data=Price(target_price=3000, weight=6), way=Way.down_to),
    UniqueUserRequest(request_id=2, symbol='FXSUSDT', request_data=Price(target_price=12345, weight=6), way=Way.down_to),
    UniqueUserRequest(request_id=2, symbol='ZRXUSDT', request_data=PercentOfPoint(target_percent=12345, current_price=124, weight=6), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='FLOWUSDT', request_data=PercentOfPoint(target_percent=10000, current_price=124, weight=6), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='ORNUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='SUSHIUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='MOVRUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='REIUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='DASHUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='MBOXUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='OSMOUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='ONEUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='C98USDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all),
    UniqueUserRequest(request_id=2, symbol='KAVAUSDT', request_data=PercentOfTime(target_percent=10000, period=Period.v_24h, weight=2), way=Way.all)
]


# async def main():
#     asyncio.create_task(monitoring.reset_weight())
#     asyncio.create_task(monitoring.get_response_from_server([RequestForServer(**req.__dict__) for req in reqs]))
#     asyncio.create_task(monitoring.check_all_changes())
#     await task1
#     await task3
#
#
# print(asyncio.run(monitoring.get_list_tickers()))
