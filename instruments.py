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
        self.url_candles = f'{self.url_api}/instruments/{name}/candles'
        self.sub_url = f'&price=BA&granularity={self.granularity}'
        self.candle_cache = {}

    def get_last_candles_by_count(self, count=5000):
        if count > 5000:
            count = 5000
        self.candle_cache = self.get(f"{self.url_candles}?count={count}{self.sub_url}")['candles']
        print('ok')
        return self.candle_cache

    async def get_candles_by_time(self, from_time, to_time=None):
        if to_time is None:
            self.candle_cache = self.get(f"{self.url_candles}?count=5000&from={from_time}{self.sub_url}")['candles']
        else:
            self.candle_cache = self.get(f"{self.url_candles}?from={from_time}&to={to_time}{self.sub_url}")['candles']
        print(self.duration)
        # await asyncio.sleep(0)
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

    async def get_all_candles(self, start_time=1):
        log.prn_log_info(f'Start_time:, {start_time}, {self.name},  {self.from_ts(start_time)}')
        i = 0

        while True:
            i += 1

            await self.get_candles_by_time(start_time)

            if self.candle_cache:
                print(self.candle_cache[-1])
            log.prn_log_info(f'Iteration # {i}, {self.name}, received candles: {len(self.candle_cache)}. '
                             f'Start_time:, {start_time}, {self.from_ts(start_time)}')
            if not self.candle_cache:
                log.prn_log_info(f'Candles list empty. start time: {start_time} {self.from_ts(start_time)}')
                self.__stop_iterations()
                return

            if not self.candle_cache[-1]['complete']:
                log.prn_log_info(f'Not complete candle found. Deleting candle from cache {self.candle_cache[-1]}')
                print(datetime.now().timestamp())
                print('LAST CANDLE NOT COMPLETE:', self.candle_cache[-1]['complete'], self.from_ts(self.candle_cache[-1]['time']))

                del self.candle_cache[-1]

                if self.candle_cache:
                    self.set_candles()

                self.__stop_iterations()
                return

            self.set_candles()
            await asyncio.sleep(0)
            start_time = int(float(self.candle_cache[-1]['time'])) + 5

            if start_time > datetime.now().timestamp():
                log.prn_log_info('Next start time more them time NOW')
                self.__stop_iterations()
                return

    async def get_last_candles(self):
        max_timestamp = self.conn.select_max(self.name, 'timestamp')
        max_timestamp = max_timestamp if max_timestamp is not None else 1

        print('max_timestamp in', max_timestamp, datetime.fromtimestamp(max_timestamp))
        max_timestamp = max_timestamp if max_timestamp else 1
        return await self.get_all_candles(max_timestamp + 5)

    def set_candles(self):
        candles = []
       # print('self.cache', self.candle_cache)
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
        self.conn.insert_many(self.name, candles)
        self.conn.commit()
        print('recorded ', self.name)


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

