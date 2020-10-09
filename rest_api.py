import requests
import aiohttp
import asyncio
from requests.exceptions import HTTPError
from logger import Logger
import json
from time import sleep, time
from security import auth_key
from datetime import datetime

log_rest = Logger(__name__)


class RestAPI:
    """ RestAPI class for connection with any remote API """

    def __init__(self, headers=None):
        """
        RestAPI object constructor
        :param headers: dict object -> request headers parameters
        :var self.session: object -> session for non async connection
        :var self.headers: -> request headers parameters
        :var self.params: dict object -> parameters of request
        :var self.timeout: -> request timeout in sec
        :var self.attempts: -> connection attempts count, in connection error case
        :var self.attempts_delay: -> delay between connection attempts
        :var self.duration: -> duration of last request in sec
        """
        self.session = requests.Session()
        self.headers = headers if headers else {}
        self.params = {}
        self.timeout = 30
        self.attempts = 10
        self.attempt_delay = 5
        self.duration = 0

    def __del__(self):
        """ Destructor for delete """
        self.session.close()

    def get(self, url, timeout=30):
        """
        Get response from simple HTTP non async request
        :param url: str : url string for request
        :param timeout: timeout for response
        :return: object from JSON response
        """

        for attempt in range(1, self.attempts + 1):
            try:
                start_time = time()
                response = self.session.get(url, timeout=self.timeout, headers=self.headers, params=self.params)
                self.duration = time() - start_time
                response.raise_for_status()
                if response.text:
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

    async def get_async(self, url, timeout=30):
        self.timeout = timeout
        print(f'request {url} Start')

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=self.params, timeout=self.timeout) as resp:
                    return await resp.text()
            except Exception as Err:
                print('+' * 100)
                print('ERROR ', Err)
                print('+' * 100)


if __name__ == "__main__":
    pass
    # # rest = RestAPI()
    # # print('rest.client', rest.session)
    # # print('rest.client.headers', rest.session.headers)
    # # print(time())
    # # print('rest_time', rest.duration)
    # auth = f'Bearer {auth_key}'
    # # h = {'Content-Type': 'application/json',
    # #      'Authorization': auth,
    # #      }
    # #
    # # print('rest_time', rest.duration)
    # #
    # # rest2 = RestAPI(h)
    # # print('rest2.client', rest2.session)
    # # print('rest2.client.headers', rest2.session.headers)
    # #
    # # print(rest2.get(
    # #     "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"))
    # #
    # # print('rest_time2', rest2.duration)
    # h = {'Content-Type': 'application/json',
    #      'Authorization': auth,
    #      'Accept-Datetime-Format': 'UNIX'
    #      }
    # #
    # # rest3 = RestAPI(h)
    # # print('rest2.client', rest3.session)
    # # print('rest2.client.headers', rest3.session.headers)
    # # print(rest3.get(
    # #     "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"))
    # # print('rest_time', rest3.duration)
    #
    # print('get async')
    # rest4 = RestAPI(h)
    # loop = asyncio.get_event_loop()
    # rest4.params = {'count': 5,
    #                 'price': 'B',
    #                 'granularity': 'S5'}
    #
    # instrument = ['CAD_SGD', 'GBP_NZD', 'ZAR_JPY', 'EUR_HUF', 'EUR_DKK', 'USD_MXN', 'GBP_USD', 'NZD_HKD', 'AUD_CHF', 'CAD_JPY', 'GBP_SGD', 'USD_SEK', 'AUD_HKD', 'AUD_NZD', 'AUD_JPY', 'EUR_ZAR', 'SGD_CHF', 'AUD_SGD', 'EUR_JPY', 'USD_CHF', 'USD_TRY', 'GBP_JPY', 'EUR_CZK', 'CHF_ZAR', 'EUR_TRY', 'USD_JPY', 'USD_NOK', 'TRY_JPY', 'USD_DKK', 'CHF_JPY', 'EUR_PLN', 'SGD_JPY', 'AUD_CAD', 'NZD_USD', 'EUR_CHF', 'NZD_SGD', 'USD_HKD', 'CHF_HKD', 'USD_CAD', 'USD_CNH', 'USD_CZK', 'GBP_ZAR', 'EUR_HKD', 'HKD_JPY', 'EUR_AUD', 'USD_SGD', 'EUR_SEK', 'GBP_HKD', 'EUR_NZD', 'EUR_CAD', 'USD_HUF', 'NZD_CAD', 'EUR_SGD', 'AUD_USD', 'EUR_USD', 'GBP_AUD', 'USD_PLN', 'SGD_HKD', 'CAD_HKD', 'GBP_CAD', 'USD_SAR', 'GBP_PLN', 'EUR_NOK', 'NZD_CHF', 'USD_ZAR', 'NZD_JPY', 'USD_THB', 'GBP_CHF', 'EUR_GBP', 'CAD_CHF']
    # # instrument = ['EUR_USD']
    # url = 'https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles'
    # url2 = 'https://api-fxpractice.oanda.com/v3/instruments/GBP_USD/candles'
    # url3 = 'https://api-fxpractice.oanda.com/v3/instruments/GBP_JPY/candles'
    #
    # async def prnres(url):
    #     rest5 = RestAPI(h)
    #     rest5.params = {'count': 5,
    #                     'price': 'B',
    #                     'granularity': 'S5'}
    #     res = await rest5.get_async(url)
    #     res = json.loads(res)['candles']
    #     print("ressss", res)
    #     print(len(res))
    #
    #
    # task = [loop.create_task(prnres(f'https://api-fxpractice.oanda.com/v3/instruments/{instr}/candles')) for instr in instrument]
    #
    # start_time = datetime.now().timestamp()
    # # loop.run_until_complete(asyncio.gather(rest4.get_async(url), rest4.get_async(url2), rest4.get_async(url3)))
    # loop.run_until_complete(asyncio.wait(task))
    # print('Time:', datetime.now().timestamp() - start_time)
