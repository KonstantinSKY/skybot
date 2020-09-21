import json
import requests
from requests.exceptions import HTTPError
import logger
import security
from time import sleep, time

log = logger.log(__name__)


class RestAPI:

    def __init__(self, headers=None):
        self.client = requests.Session()
        self.client.headers = headers if headers else {}
        self.timeout = 0
        self.attempts = 10
        self.attempt_delay = 5
        self.duration = 0

    def get(self, url, timeout=30):
        self.timeout = timeout

        for attempt in range(1, self.attempts + 1):
            try:
                start_time = time()
                response = self.client.get(url, timeout=self.timeout)
                self.duration = time() - start_time
                response.raise_for_status()
                return response

            except HTTPError as http_err:
                log.error(f'HTTP error occurred: {http_err}, attempt:{attempt}, duration:{self.duration}')
                print(f'HTTP error occurred: {http_err}')
                if response.status_code < 500:
                    return None
                sleep(self.attempt_delay)
            except Exception as err:
                log.error(f' Error occurred {err}, attempt:{attempt}')
                return None


if __name__ == "__main__":
    rest = RestAPI()
    print('rest.client', rest.client)
    print('rest.client.headers', rest.client.headers)
    print(time())
    print('rest_time', rest.duration)
    h = {'Content-Type': 'application/json',
         'Authorization': 'Bearer c86eb218936e2b01ec5a52a729e17cae-963352d561978c294ce4b680e3335a03',
         }

    print('rest_time', rest.duration)

    rest2 = RestAPI(h)
    print('rest2.client', rest2.client)
    print('rest2.client.headers', rest2.client.headers)

    print(rest2.get(
        "https://api-fxpractice.oanda.com/v37/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"))

    print('rest_time2', rest2.duration)
    h = {'Content-Type': 'application/json',
         'Authorization': 'Bearer c86eb218936e2b01ec5a52a729e17cae-963352d561978c294ce4b680e3335a03',
         'Accept-Datetime-Format': 'UNIX'
         # 'Accept-Datetime-Format': 'RFC3339'
         }

    rest3 = RestAPI(h)
    print('rest2.client', rest3.client)
    print('rest2.client.headers', rest3.client.headers)
    print(rest3.get(
        "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"))
    print('rest_time', rest3.duration)