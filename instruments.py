from oanda_api import OandaAPI
from security import oanda_auth_keys
from datetime import datetime
from logger import Logger
from time import sleep

log = Logger(__name__)


class Instrument(OandaAPI):

    def __init__(self, auth, name, granularity):
        super().__init__(auth)
        self.name = name
        self.granularity = granularity
        self.url_candles = f'{self.url_api}/instruments/{name}/candles'
        self.sub_url = f'&price=BA&granularity={self.granularity}'
        self.cache = {}
        self.candles = {}

    def get_last_candles_by_count(self, count=5000):
        if count > 5000:
            count = 5000
        self.cache = self.get(f"{self.url_candles}?count={count}{self.sub_url}")['candles']
        return self.cache

    def get_candles_by_time(self, from_time, to_time=None):
        if to_time is None:
            self.cache = self.get(f"{self.url_candles}?count=5000&from={from_time}{self.sub_url}")['candles']
        else:
            self.cache = self.get(f"{self.url_candles}?from={from_time}&to={to_time}{self.sub_url}")['candles']
        return self.cache

    def __stop_iterations(self):
        log.prn_log_info(f'The Getting is stopped.')
        log.prn_log_info(f'Added total candles: {len(self.cache)}')
        log.prn_log_info(f'Request duration: {self.duration}')
        last_timestamp = self.conn.select_max(self.name, 'timestamp')
        log.prn_log_info(f'last_time in DB: {last_timestamp} {self.from_ts(last_timestamp)}')
        if self.cache:
            last_time = self.cache[-1]['time']
            log.prn_log_info(f'Last candle time in cache: {last_time}, {self.from_ts(last_time)}')

    def get_all_candles(self, start_time=1):
        log.prn_log_info(f'Start_time:, {start_time}, {self.from_ts(start_time)}')
        i = 0
        while True:
            i += 1

            self.get_candles_by_time(start_time)

            if self.cache:
                print(self.cache[-1])
            log.prn_log_info(f'Iteration # {i}, received candles: {len(self.cache)}. '
                             f'Start_time:, {start_time}, {self.from_ts(start_time)}')
            if not self.cache:
                log.prn_log_info(f'Candles list empty. start time: {start_time} {self.from_ts(start_time)}')
                self.__stop_iterations()
                return

            if not self.cache[-1]['complete']:
                log.prn_log_info(f'Not complete candle found. Deleting candle from cache {self.cache[-1]}')
                print(datetime.now().timestamp())
                print('LAST CANDLE NOT COMPLETE:', self.cache[-1]['complete'], self.from_ts(self.cache[-1]['time']))

                del self.cache[-1]

                if self.cache:
                    self.set_candles()

                self.__stop_iterations()
                return

            self.set_candles()

            start_time = int(float(self.cache[-1]['time'])) + 5

            if start_time > datetime.now().timestamp():
                log.prn_log_info('Next start time more them time NOW')
                self.__stop_iterations()
                return

    def get_last_candles(self):
        max_timestamp = self.conn.select_max(self.name, 'timestamp')
        max_timestamp = max_timestamp if max_timestamp is not None else 1

        print('max_timestamp in', max_timestamp, datetime.fromtimestamp(max_timestamp))
        max_timestamp = max_timestamp if max_timestamp else 1
        return self.get_all_candles(max_timestamp + 5)

    def set_candles(self):
        candles = []
        print('self.cache', self.cache)
        for candle in self.cache:
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
        print('candles record ', candles)
        self.conn.insert_many(self.name, candles)
        self.conn.commit()


if __name__ == "__main__":
    inst = Instrument(oanda_auth_keys[1], 'EUR_USD', 'S5')
    print(inst.get_last_candles_by_count(2))
    # print(inst.get_candles_by_time(1))
    print(datetime.fromtimestamp(1600759075))
    print(datetime.fromtimestamp(1))
    #print(datetime.fromtimestamp(1086037195))
    #inst.get_all_candles()

    inst.get_last_candles()
    print(inst.conn.select_max(inst.name, 'timestamp'), datetime.now().timestamp(), 'delta', datetime.now().timestamp()-inst.conn.select_max(inst.name, 'timestamp'))
    while True:
        last_time = datetime.now().timestamp() // 5 * 5
        print('last_time', last_time)
        next_time = last_time + 5
        print('next_time', next_time)
        sleep_time = next_time - datetime.now().timestamp()
        print('sleep_time', sleep_time)

        sleep(sleep_time)
        print('check_time', datetime.now().timestamp())
        if datetime.now().timestamp() < next_time:
            print('CONTUNUE>>>')
            continue
        print(datetime.now().timestamp())
        inst.get_last_candles()

