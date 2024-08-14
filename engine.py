import config as cfg

from binance import Client
from fastapi import FastAPI

from utils.rabbitmq import RabbitMq
from utils.repositories import Repository
from utils.service import Monitoring


repo = Repository()
rabbit = RabbitMq(cfg.RABBITMQ_USER, cfg.RABBITMQ_PASSWORD, cfg.RABBITMQ_QUEUE, cfg.RABBITMQ_HOST, cfg.RABBITMQ_PORT)
binance_bot = Client(api_key=cfg.BINANCE_API_KEY, api_secret=cfg.BINANCE_API_SECRET)

monitoring = Monitoring(binance_bot, repo, rabbit)
app = FastAPI()
