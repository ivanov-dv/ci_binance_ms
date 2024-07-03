import time
from engine import *
import utils.assist as assist


def main():

    while True:
        print('Iteration...')
        unique_requests_for_server = req_repo.do_unique_requests_for_server()
        user_unique_requests = tuple(req_repo.unique_user_requests.keys())
        print('Requests weight: ', req_repo.requests_weight)
        response = monitoring.get_response_from_server(unique_requests_for_server)

        res = monitoring.check_all_changes(user_unique_requests, response)

        if res:
            print(res)

        time.sleep(1)


if __name__ == "__main__":
    assist.check_proxies(cfg.PROXIES)
    main()
