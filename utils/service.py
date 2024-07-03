import binance
import logging
import threading
import time

import config
from utils.models import (
    UserRequest,
    TypeRequest,
    Way,
    Symbol,
    ResponseKline,
    Period,
    ResponseGetTicker,
    Price,
    PercentOfPoint,
    PercentOfTime, RequestForServer)


class Monitoring:
    """
    Класс для осуществления мониторинга запросов пользователей.
    """

    def __init__(self, client: binance.Client):
        self.client = client
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

    def _get_response_price_or_percent_of_point(self, request: RequestForServer) -> None:
        for _ in range(config.TRY_GET_RESPONSE):
            try:
                response = self.client.get_klines(
                    symbol=request.symbol,
                    interval=config.INTERVAL_FOR_PRICE_REQUEST,
                    limit=config.LIMIT_FOR_PRICE_REQUEST
                )
                list_response = [ResponseKline(*map(float, i[:11])) for i in response]
                self.response_from_server[TypeRequest.price].update({request.symbol: list_response})
                break
            except Exception as e:
                time.sleep(config.TIMEOUT_BETWEEN_RESPONSE)
                str(e)
                continue

    def _get_response_percent_of_time(self, request: RequestForServer) -> None:
        for _ in range(config.TRY_GET_RESPONSE):
            try:
                response = self.client.get_ticker(symbol=request.symbol)
                if not (request.symbol in response):
                    self.response_from_server[TypeRequest.period].update({request.symbol: {}})
                self.response_from_server[TypeRequest.period][request.symbol].update(
                    {request.data_request.period: ResponseGetTicker(response)}
                )
                break
            except Exception as e:
                time.sleep(config.TIMEOUT_BETWEEN_RESPONSE)
                str(e)
                continue

    def _check_change(
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
            user_requests: tuple | list,
            response_from_server: dict[TypeRequest, {str, list[ResponseKline]} | {str, dict[Period, ResponseGetTicker]}]
    ):
        """
        Проверяет все запросы на изменение.

        Args:
            user_requests: Список или кортеж запросов
            response_from_server: Ответ сервера в Dict.

        Returns: Возвращает множество Set с запросами, достигшими необходимых значений.
        """

        res = set()

        for request in user_requests:
            if self._check_change(request, response_from_server):
                res.add(request)
        return res

    def get_response_from_server(
            self,
            requests_for_server: set[RequestForServer]
    ) -> dict[TypeRequest, {str, list[ResponseKline]} | {str, dict[Period, ResponseGetTicker]}]:
        """
        Получает ответы от сервера по множеству запросов в многопоточном режиме.

        Args:
            requests_for_server: Перечень уникальных запросов на сервер в виде множества set.

        Returns: Ответ сервера в Dict
        """

        tasks = []
        self.response_from_server = {TypeRequest.price: {}, TypeRequest.period: {}}

        for request in requests_for_server:
            if isinstance(request.data_request, (Price, PercentOfPoint)):
                t = threading.Thread(target=self._get_response_price_or_percent_of_point, args=(request,))
                tasks.append(t)
            if isinstance(request.data_request, PercentOfTime) and request.data_request.period == Period.v_24h:
                t = threading.Thread(target=self._get_response_percent_of_time, args=(request,))
                tasks.append(t)

        for task in tasks:
            task.start()
            time.sleep(config.THREAD_INTERVAL_BETWEEN_RESPONSE)
        for task in tasks:
            task.join()

        return self.response_from_server
