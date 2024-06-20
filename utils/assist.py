import logging
import os
import requests


class Proxies:
    @staticmethod
    def get():
        res = {}
        if 'PROXIES' in os.environ:
            for pos, proxy in enumerate(os.environ['PROXIES'].split(',')):
                res.update({pos: {'http': f'http://{proxy}', 'https': f'https://{proxy}'}})
        return res

    @staticmethod
    def check(proxies):
        response = requests.get("http://httpbin.org/ip", timeout=10)
        logging.info(f"Base IP: {response.json()['origin']}")

        for proxies in proxies.values():
            response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
            logging.info(f'Proxy {response.json()["origin"]} - ok')
        logging.info('Proxy tests completed.') if proxies else logging.info('No proxies provided.')