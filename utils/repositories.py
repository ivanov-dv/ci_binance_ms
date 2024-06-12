import binance
import threading

import config


from typing_extensions import Self

from utils.models import *
from utils.patterns import PatternSingleton, RepositoryDB


class SessionRepository(RepositoryDB, PatternSingleton):
    sessions = {}

    def _add(self, session: Session):
        pass

    def _delete(self, session: Session):
        pass

    def get(self, session: Session):
        pass

    def update(self, session: Session):
        pass


class RequestRepository(RepositoryDB, PatternSingleton):
    user_requests: dict[int, set[UserRequest]] = {}
    unique_user_requests: dict[UserRequest, set[int]] = {}
    unique_requests_for_server: set[RequestForServer] = set()

    def _delete_unique_user_request(self, user_id: int, request: UserRequest) -> None:
        if request in self.unique_user_requests:
            self.unique_user_requests[request].discard(user_id)
            if not self.unique_user_requests[request]:
                self.unique_user_requests.pop(request, None)

    def add(self, user_id: int, request: UserRequest) -> Self:

        if user_id in self.user_requests:
            self.user_requests[user_id].add(request)
        else:
            self.user_requests.update({user_id: {request}})

        if request in self.unique_user_requests:
            self.unique_user_requests[request].add(user_id)
        else:
            self.unique_user_requests.update({request: {user_id}})

        return self

    def delete(self, user_id: int, request: UserRequest) -> Self:
        if user_id in self.user_requests:
            self.user_requests[user_id].discard(request)
            if not self.user_requests[user_id]:
                self.user_requests.pop(user_id, None)
        self._delete_unique_user_request(user_id, request)
        return self

    def update_time_request(self, user_id: int, request: UserRequest) -> Self:
        """
        Обновляет время изменения запроса.
        """

        list_requests = list(self.user_requests[user_id])
        list_requests[list_requests.index(request)].time_info.update_time = dt.utcnow()
        list_requests[list_requests.index(request)].time_info.update_time_unix = time.time()
        self.user_requests[user_id] = set(list_requests)
        return self

    def get(self, user_id: int, request: UserRequest) -> UserRequest | None:
        return request if user_id in self.user_requests and request in self.user_requests[user_id] else None

    def get_all_for_user_id(self, user_id: int) -> set[UserRequest] | None:
        return self.user_requests[user_id] if user_id in self.user_requests else None

    def do_unique_requests_for_server(self) -> set[RequestForServer]:
        """
        Создает словарь с уникальными запросами (без дублей) на API.
        Сортирует запросы по ключам TypeRequest.percent и TypedRequest.price.

        :return: Set[RequestForServer]
        """

        self.unique_requests_for_server = set(map(RequestForServer, self.unique_user_requests.keys()))

        return self.unique_requests_for_server


class ResponseRepository(RepositoryDB, PatternSingleton):

    def __init__(self, db, client: binance.Client):
        super().__init__(db)
        self.client = client
        self.response = None

    def _get_response_price_or_percent_of_point(self, request: RequestForServer) -> None:
        for _ in range(config.TRY_GET_RESPONSE):
            try:
                response = self.client.get_klines(
                    symbol=request.symbol,
                    interval=config.INTERVAL_FOR_PRICE_REQUEST,
                    limit=config.LIMIT_FOR_PRICE_REQUEST
                )
                list_response = [ResponseKline(*map(float, i[:11])) for i in response]
                self.response[TypeRequest.price].update({request.symbol: list_response})
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
                    self.response[TypeRequest.period].update({request.symbol: {}})
                self.response[TypeRequest.period][request.symbol].update(
                    {request.data_request.period: ResponseGetTicker(response)}
                )
                break
            except Exception as e:
                time.sleep(config.TIMEOUT_BETWEEN_RESPONSE)
                str(e)
                continue

    def get_response_from_server(
            self,
            requests: set[RequestForServer]
    ) -> dict[TypeRequest, {str, list[ResponseKline]} | {str, dict[Period, ResponseGetTicker]}]:
        """
        Получает ответы от сервера по множеству запросов в многопоточном режиме.

        Args:
            requests: Перечень уникальных запросов на сервер в виде множества set.

        Returns: Ответ сервера в Dict
        """

        tasks = []
        self.response = {TypeRequest.price: {}, TypeRequest.period: {}}

        for request in requests:
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

        return self.response
