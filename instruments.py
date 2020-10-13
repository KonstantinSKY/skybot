from oanda_api import OandaAPI
from security import oanda_auth_keys
from datetime import datetime
from logger import Logger
from time import sleep
import asyncio

log = Logger(__name__)


class Instrument(OandaAPI):
    """
    Instrument candle class, inherits from class Oanda_api
    Works with Oanda API
    """

    def __init__(self, auth, name, granularity):
        """
        Oanda instrument object constructor
        :param auth: str -> Security
        :param name: str -> Instrument name, for example "EUR_USD"
        :param granularity: str ->   Instrument granularity or candle timeframe
        :var self.url_candles: str -> Main URL, self.url_api inherits from Oanda_API
        :var self.sub_url: srt -> Sub url string with price Type (BA) and timeframe
        :var self.candle_caсhe: dict -> Temporary storage for received candles
        """
        super().__init__(auth)
        self.name = name
        self.granularity = granularity
        self.url_candles = f'{self.url_api}instruments/{name}/candles'
        self.candle_cache = {}

        max_timestamp = self.conn.select_max(self.name, 'timestamp')
        max_timestamp = max_timestamp + 5 if max_timestamp else 1
        self.params = {'price': 'BA',
                       'granularity': 'S5',
                       'count': 5000,
                       'from': max_timestamp}
        self.iter = 0

        print('self.params', self.params)
        print('time for start', self.from_ts(max_timestamp))

    def get_last_candles_by_count(self, count=5000):
        if count > 5000:
            count = 5000
        self.candle_cache = self.get(f"{self.url_candles}")['candles']
        print('ok')
        return self.candle_cache

    def get_candles_by_time(self, from_time, to_time=None):
        start_time = datetime.now().timestamp()
        if to_time is None:
            self.candle_cache = self.get(f"{self.url_candles}?count=5000&from={from_time}")['candles']
        else:
            self.candle_cache = self.get(f"{self.url_candles}?from={from_time}&to={to_time}")['candles']
        print('time for response', datetime.now().timestamp() - start_time)
        print(f"1.time for:{self.name}:{self.duration}")
        print(f"2.time for:{self.name}:{self.duration}")

        return

    def __stop_iterations(self):
        log.prn_log_info(f'The Getting is stopped.')
        log.prn_log_info(f'Added total candles: {len(self.candle_cache)}')
        log.prn_log_info(f'Request duration: {self.duration}')
        last_timestamp = self.conn.select_max(self.name, 'timestamp')
        log.prn_log_info(f'last_time in DB: {last_timestamp} {self.from_ts(last_timestamp)}')
        if self.candle_cache:
            last_time = self.candle_cache[-1]['time']
            log.prn_log_info(f'Last candle time in cache: {last_time}, {self.from_ts(last_time)}')

    def get_last_candles(self):
        """ Get all last candles"""
        while True:
            self.candle_cache = self.get(f"{self.url_candles}")['candles']
            self.verify_candles()
            if self.candle_cache:
                self.set_candles()
            self.waiter()

    def waiter(self):
        log.prn_log_info(f'Waiter: Next start time: {self.params["from"]})')
        log.prn_log_info(f'Now:  {datetime.now().timestamp()} {datetime.now()} ')

        if (datetime.now().timestamp() - int(float(self.params['from']))) < 60:
            check_time = datetime.now().timestamp() // 5 * 5 + 5
            log.prn_log_info(f'NEED TO sleep: {check_time - datetime.now().timestamp()}')
            sleep(check_time - datetime.now().timestamp())

    def verify_candles(self):
        self.iter += 1
        start_time = self.params["from"]
        log.prn_log_info(f'Iteration # {self.iter}, {self.name}, Start_time:, {start_time}, {self.from_ts(start_time)}')

        if not self.candle_cache:
            log.prn_log_info(f'Candles is absolutely empty. start time: {start_time} {self.from_ts(start_time)}')
            self.params["from"] = int(datetime.now().timestamp()) // 5 * 5 - 5
            log.prn_log_info(f'Next start tine: {self.params["from"]}')
            return
        # check for -2 items complete
        if len(self.candle_cache) > 1:
            print('checking [-2]', self.candle_cache[-2])
            if not self.candle_cache[-2]['complete']:
                log.prn_log_info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                quit()

        print('checking', self.candle_cache[-1])
        if not self.candle_cache[-1]['complete']:
            self.params["from"] = self.candle_cache[-1]['time']
            del self.candle_cache[-1]
            if not self.candle_cache:
                log.prn_log_info(f'Candles is empty. start time: {self.params["from"]} '
                                 f'{self.from_ts(self.params["from"])},  Now: {datetime.now().timestamp()}')
            print('Next start time:', self.params["from"])
            print('Candle got', self.candle_cache)
            return

        log.prn_log_info(f'Iteration # {self.iter}, {self.name}, received candles: {len(self.candle_cache)}.'
                         f' Now: {datetime.now().timestamp()}')
        self.params["from"] = int(float(self.candle_cache[-1]['time'])) + 5
        print('Next start time:', self.params["from"])
        log.prn_log_info(f'Candle COUNT:  {len(self.candle_cache)}')
        log.prn_log_info(f'from start time: {start_time} to  {int(float(self.candle_cache[-1]["time"]))}')
        print('Candle got', self.candle_cache[-1])

    def set_candles(self):
        candles = []
        for candle in self.candle_cache:
            candles.append({
                'timestamp': int(float(candle['time'])),
                'bid_high': candle['bid']['h'],
                'bid_low': candle['bid']['l'],
                'bid_open': candle['bid']['o'],
                'bid_close': candle['bid']['c'],
                'ask_high': candle['ask']['h'],
                'ask_low': candle['ask']['l'],
                'ask_open': candle['ask']['o'],
                'ask_close': candle['ask']['c'],
                'volume': candle['volume']
            }
            )
        self.conn.insert_many(self.name, candles, 'timestamp')
        self.conn.conn.commit()
        print('recorded ', self.name)


if __name__ == "__main__":
    inst = Instrument(oanda_auth_keys[1], 'GBP_USD', 'S5')
    # print(inst.get_last_candles_by_count(2))
    # # print(inst.get_candles_by_time(1))
    # print(datetime.fromtimestamp(1600759075))
    # print(datetime.fromtimestamp(1))
    # #print(datetime.fromtimestamp(1086037195))
    # #inst.get_all_candles()
    #
    inst.get_last_candles()

    # print(inst.conn.select_max(inst.name, 'timestamp'), datetime.now().timestamp(), 'delta', datetime.now().timestamp()-inst.conn.select_max(inst.name, 'timestamp'))
    # while True:
    #
    #     last_time = datetime.now().timestamp() // 5 * 5
    #     print('last_time', last_time)
    #     next_time = last_time + 5
    #     print('next_time', next_time)
    #     sleep_time = next_time - datetime.now().timestamp()
    #     print('sleep_time', sleep_time)
    #     sleep(sleep_time)
    #     print('check_time', datetime.now().timestamp())
    #     if datetime.now().timestamp() < next_time:
    #         print('CONTUNUE>>>')
    #         continue
    #     print(datetime.now().timestamp())
    #     inst.get_last_candles()
