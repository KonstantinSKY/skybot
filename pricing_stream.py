from account import Account
from security import oanda_auth_keys
from logger import Logger
import json
import redis
from datetime import datetime

log = Logger(__name__)


class PricingStream(Account):

    def __init__(self, auth, acc_id, ticker_names):
        super().__init__(auth, acc_id)
        self.db = redis.Redis('127.0.0.1', '6379')
        self.url_pricing_stream = f'{self.url_stream}accounts/{acc_id}/pricing/stream?instruments='
        log.log_info('Pricing Init')
        print(self.url_pricing_stream)
        del self.client.headers['Content-Type']
        del self.client.headers['Accept - Encoding']
        self.ticker_names = ticker_names
        self.client.stream = True
        self.client.verify = True
        print(self.client.headers)

    def stream(self, instruments):
        while True:
            try:
                instr_str = "%2C".join(instruments)
                print(instr_str)
                self.__push_lines(self.get_stream(f'{self.url_pricing_stream}{instr_str}'))
            except Exception as err:
                log.prn_log_err(f'ERROR:{err}')
                continue

    def __push_lines(self, response):
        for line in response.iter_lines(1):
            line_obj = json.loads(line)
            print(line)
            print('delta', datetime.now().timestamp() - float(line_obj['time']))
            for ticker_name in self.ticker_names:
                self.db.rpush(f'{ticker_name}:prices', line)


if __name__ == "__main__":
    price = PricingStream(oanda_auth_keys[1], '101-001-15249313-001', ['price_1'])
    # price.stream(price.get_instruments_names(['EUR_USD']))
    price.stream(['EUR_USD'])

    #
    # min_spread = 1
    # max_spread = 0
    #
    #         bids = [bid['price'] for bid in line_obj['bids']]
    #         asks = [ask['price'] for ask in line_obj['asks']]
    #         print(bids)
    #         print(asks)
    #         price_json = json.dumps({line_obj['time']: {
    #                         'bids': bids,
    #                         'asks': asks
    #                          }})
    #         # db.rpush('1:eur_usd', price_json)
    #         db.rpush('1:eur_usd', line)
    #
    #         #print('db_pop', db.lpop('1:eur_usd'))
    #
    #         print(line_obj['instrument'])
    #         print(line_obj['time'], price.from_ts(line_obj['time']))
    #         for bid in line_obj['bids']:
    #             print('bid:', bid['price'])
    #         for ask in line_obj['asks']:
    #             print('ask:', ask['price'])
    #         spread = 0
    #         for key in range(len(line_obj['asks'])):
    #             spread = float(line_obj['asks'][key]['price']) - float(line_obj['bids'][key]['price'])
    #             print('spread:', spread)
    #         if min_spread > spread:
    #             min_spread = spread
    #         if max_spread < spread:
    #             max_spread = spread
    #         print('min_spread:', min_spread)
    #         print('max_spread:', max_spread)

    print('END')
