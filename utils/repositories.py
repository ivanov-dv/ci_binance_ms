import httpx

from config import REPO_HOST
from utils.models import UniqueUserRequest, RequestForServer
from utils.patterns import PatternSingleton


class Requests:
    @staticmethod
    async def get(endpoint: str):
        async with httpx.AsyncClient() as client:
            return await client.get(endpoint)

    @staticmethod
    async def post(endpoint: str, data):
        async with httpx.AsyncClient() as client:
            return await client.post(endpoint, data=data)

    @staticmethod
    async def put(endpoint: str, data):
        async with httpx.AsyncClient() as client:
            return await client.put(endpoint, data=data)

    @staticmethod
    async def delete(endpoint: str):
        async with httpx.AsyncClient() as client:
            return await client.delete(endpoint)


class Repository(PatternSingleton):
    unique_user_requests: list[UniqueUserRequest] = []
    unique_requests_for_server: list[RequestForServer] = []
    requests_weight: int = 0

    async def load_requests_from_remote_repo(self):
        unique_user_requests = await Requests.get(f'{REPO_HOST}/requests/unique/')
        unique_requests_for_server = await Requests.get(f'{REPO_HOST}/requests/server/')
        self.unique_user_requests = [UniqueUserRequest(**req) for req in unique_user_requests.json()]
        self.unique_requests_for_server = [RequestForServer(**req) for req in unique_requests_for_server.json()]

    async def get_unique_requests_for_server(self):
        return self.unique_requests_for_server

    async def get_unique_user_requests(self):
        return self.unique_user_requests

    @staticmethod
    async def get_users_for_request(request_id: int):
        res = await Requests.get(f'{REPO_HOST}/users/requests/{request_id}')
        return res.json()

    @staticmethod
    async def delete_request_for_user(user_id, request_id):
        res = await Requests.delete(f'{REPO_HOST}/requests/{user_id}?request_id={request_id}')
        return res
