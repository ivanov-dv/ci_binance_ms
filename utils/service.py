import logging

import binance

from utils.models import *


class Monitoring:
    """
    Класс для осуществления мониторинга запросов пользователей.
    """

    def __init__(self, bot: binance.Client):
        self.bot = bot
        self.response_from_server = None

    def _price_check_change(self, request: UserRequest, response: dict) -> UserRequest | None:
        try:
            klines = response[TypeRequest.price][request.symbol]
            if request.way == Way.up_to:
                max_price = max([kline.high_price for kline in klines])
                if request.data_request.target_price <= max_price:
                    return request
            if request.way == Way.down_to:
                min_price = min([kline.low_price for kline in klines])
                if request.data_request.target_price >= min_price:
                    return request
        except Exception as e:
            logging.exception(f'{self.__class__.__qualname__} - {e}')

    def _percent_of_point_check_change(self, request: UserRequest, response: dict) -> UserRequest | None:
        try:
            klines = response[TypeRequest.price][request.symbol]
            if request.way in (Way.up_to, Way.all):
                max_price = max([kline.high_price for kline in klines])
                delta = max_price - request.data_request.current_price
                if delta / request.data_request.current_price * 100 >= request.data_request.target_percent:
                    return request
            if request.way in (Way.down_to, Way.all):
                min_price = min([kline.low_price for kline in klines])
                delta = request.data_request.current_price - min_price
                if delta / request.data_request.current_price * 100 >= request.data_request.target_percent:
                    return request
        except Exception as e:
            logging.exception(f'{self.__class__.__qualname__} - {e}')

    def _percent_of_time_check_change(self, request: UserRequest, response: dict) -> UserRequest | None:
        try:
            ticker = response[TypeRequest.period][request.symbol][request.data_request.period]
            if request.way == Way.up_to:
                if ticker.price_change_percent >= request.data_request.target_percent:
                    return request
            elif request.way == Way.down_to:
                if ticker.price_change_percent <= -request.data_request.target_percent:
                    return request
            else:
                if abs(ticker.price_change_percent) >= request.data_request.target_percent:
                    return request
        except Exception as e:
            logging.exception(f'{self.__class__.__qualname__} - {e}')

    def check_change(
            self,
            request: UserRequest,
            response_from_server: dict[TypeRequest, {Symbol, ResponseKline} | {Symbol, dict[Period, ResponseGetTicker]}]
    ):
        """
        Проверяет один запрос на изменение.

        Args:
            request: Запрос
            response_from_server: Ответ сервера в Dict

        Returns: Возвращает запрос, если он достиг или превысил значения.
        """

        if isinstance(request.data_request, Price):
            return self._price_check_change(request, response_from_server)

        if isinstance(request.data_request, PercentOfPoint):
            return self._percent_of_point_check_change(request, response_from_server)

        if isinstance(request.data_request, PercentOfTime):
            return self._percent_of_time_check_change(request, response_from_server)

    def check_all_changes(
            self,
            requests: tuple | list,
            response_from_server: dict[TypeRequest, {Symbol, ResponseKline} | {Symbol, dict[Period, ResponseGetTicker]}]
    ):
        """
        Проверяет все запросы на изменение.

        Args:
            requests: Список или кортеж запросов
            response_from_server: Ответ сервера в Dict

        Returns: Возвращает множество Set с запросами, достигшими необходимых значений.
        """

        res = set()
        for request in requests:
            if self.check_change(request, response_from_server) is not None:
                res.add(request)
        return res
