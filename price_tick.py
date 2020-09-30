import json
from datetime import datetime
from databases import ConnectDB


class Tick:
    db_path = "DB/oanda.sqlite"

    def __init__(self, instrument):
        self.conn = ConnectDB(Tick.db_path)
        self.instrument = instrument
        self.bots = {}
        # bots_inits
        self.sync_flag = False
        self.ticks = []
        self.candles = {}
        self.start_candles = {}
        self.last_candles = [{'timestamp': 1,
                              'bid': {
                                  'open': 0,
                                  'close': 0,
                                  'high': 0,
                                  'low': 0
                              },
                              'ask': {
                                  'open': 0,
                                  'close': 0,
                                  'high': 0,
                                  'low': 0
                              },
                              'volume': 0
                              }]

    def start(self, price_obj):
        # print('price_line', price_obj)
        self.__parse_price(price_obj)

    def __parse_price(self, price_obj):
        for i in range(len(price_obj['bids'])):
            self.ticks.append({
                'time': float(price_obj['time']),
                'bid': float(price_obj['bids'][i]['price']),
                'ask': float(price_obj['asks'][i]['price'])
            })
            self.__update_last_candle()
        # print("price time", self.ticks[-1]['time'])
        # print("time now", datetime.now().timestamp())
        # print("delta", datetime.now().timestamp()-self.ticks[-1]['time'])

    def __update_last_candle(self):
        timestamp = int(self.ticks[-1]['time'] // 5 * 5)
        # print(datetime.fromtimestamp(timestamp))
        if timestamp != self.last_candles[0]['timestamp']:
            print('New candle')
            candle = {'timestamp': timestamp,
                      'bid': {
                          'open': self.ticks[-1]['bid'],
                          'close': self.ticks[-1]['bid'],
                          'high': self.ticks[-1]['bid'],
                          'low': self.ticks[-1]['bid']
                      },
                      'ask': {
                          'open': self.ticks[-1]['ask'],
                          'close': self.ticks[-1]['ask'],
                          'high': self.ticks[-1]['ask'],
                          'low': self.ticks[-1]['ask']
                      },
                      'volume': 1
                      }

            self.last_candles.insert(0, candle)
            if len(self.last_candles) == 3:
                del self.last_candles[2]
            print(timestamp)
            print('self.last_candles', self.last_candles)
            return

        if self.last_candles[0]['ask']['high'] < self.ticks[-1]['ask']:
            self.last_candles[0]['ask']['high'] = self.ticks[-1]['ask']
        if self.last_candles[0]['ask']['low'] > self.ticks[-1]['ask']:
            self.last_candles[0]['ask']['low'] = self.ticks[-1]['ask']

        if self.last_candles[0]['bid']['high'] < self.ticks[-1]['bid']:
            self.last_candles[0]['bid']['high'] = self.ticks[-1]['bid']
        if self.last_candles[0]['bid']['low'] > self.ticks[-1]['bid']:
            self.last_candles[0]['bid']['low'] = self.ticks[-1]['bid']

        self.last_candles[0]['ask']['close'] = self.ticks[-1]['ask']
        self.last_candles[0]['bid']['close'] = self.ticks[-1]['bid']
        self.last_candles[0]['volume'] += 1
        print('self.last_candles', self.last_candles)

    def __bot_farm(self):
        pass


if __name__ == "__main__":
    tick = Tick("EUR_USD")
    tick.start()
