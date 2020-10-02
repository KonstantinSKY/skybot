import requests
from requests.exceptions import HTTPError
from logger import Logger
import json
from time import sleep, time
from security import auth_key

log_rest = Logger(__name__)


class RestAPI:
    """ RestAPI class for connection with any remote API """

    def __init__(self, headers=None):
        """
        RestAPI object constructor
        :param headers: dict object -> request headers parameters
        :var self.session: object -> session for non async connection
        :var self.headers: -> request headers parameters
        :var self.timeout: -> request timeout in sec
        :var self.attempts: -> connection attempts count, in connection error case
        :var self.attempts_delay: -> delay between connection attempts
        :var self.duration: -> duration of request in sec
        """
        self.session = requests.Session()
        self.headers = headers if headers else {}
        self.timeout = 0
        self.attempts = 10
        self.attempt_delay = 5
        self.duration = 0

    def __del__(self):
        self.session.close()

    def get(self, url, timeout=30):
        self.timeout = timeout

        for attempt in range(1, self.attempts + 1):
            try:
                start_time = time()
                response = self.session.get(url, timeout=self.timeout, headers=self.headers)
                self.duration = time() - start_time
                response.raise_for_status()
                # if
                return json.loads(response.text)

            except HTTPError as http_err:
                log_rest.prn_log_err(f'HTTP error occurred: {http_err}, attempt:{attempt}, duration:{self.duration}')
                sleep(self.attempt_delay)
            except Exception as err:
                log_rest.prn_log_err(f' Error occurred {err}, attempt:{attempt}')

    def get_stream(self, url, timeout=30):
        self.timeout = timeout

        for attempt in range(1, self.attempts + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response

            except HTTPError as http_err:
                log_rest.prn_log_err(f'HTTP error occurred: {http_err}, attempt:{attempt}, duration:{self.duration}')
                sleep(self.attempt_delay)
            except Exception as err:
                log_rest.prn_log_err(f' Error occurred {err}, attempt:{attempt}')


if __name__ == "__main__":
    rest = RestAPI()
    print('rest.client', rest.session)
    print('rest.client.headers', rest.session.headers)
    print(time())
    print('rest_time', rest.duration)
    auth = f'Bearer {auth_key}'
    h = {'Content-Type': 'application/json',
         'Authorization': auth,
         }

    print('rest_time', rest.duration)

    rest2 = RestAPI(h)
    print('rest2.client', rest2.session)
    print('rest2.client.headers', rest2.session.headers)

    print(rest2.get(
        "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"))

    print('rest_time2', rest2.duration)
    h = {'Content-Type': 'application/json',
         'Authorization': auth,
         'Accept-Datetime-Format': 'UNIX'
         # 'Accept-Datetime-Format': 'RFC3339'
         }

    rest3 = RestAPI(h)
    print('rest2.client', rest3.session)
    print('rest2.client.headers', rest3.session.headers)
    print(rest3.get(
        "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"))
    print('rest_time', rest3.duration)