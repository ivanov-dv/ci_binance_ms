import binance
import threading
from typing_extensions import Self

import config
from utils.models import *
from utils.patterns import PatternSingleton, RepositoryDB


class RequestRepository(RepositoryDB, PatternSingleton):
    user_requests: dict[int, set[UserRequest]] = {}
    unique_user_requests: dict[UserRequest, set[int]] = {}
    unique_requests_for_server: set[RequestForServer] = set()
    requests_weight: int = 0

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

    def do_unique_requests_for_server(self) -> set[RequestForServer]:
        """
        Создает словарь с уникальными запросами (без дублей) на API.

        :return: Set[RequestForServer]
        """

        self.unique_requests_for_server = set()
        self.requests_weight = 0

        for request in self.unique_user_requests.keys():
            if not RequestForServer(request) in self.unique_requests_for_server:
                self.unique_requests_for_server.add(RequestForServer(request))
                self.requests_weight += request.data_request.weight

        return self.unique_requests_for_server
