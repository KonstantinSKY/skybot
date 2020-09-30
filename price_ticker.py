import json
import redis
from price_tick import Tick


class Ticker:

    def __init__(self, name, instruments=['EUR_USD']):
        self.name = name
        self.db = redis.Redis('127.0.0.1', '6379')
        self.ticks = {}
        self.instruments = instruments
        for instr in instruments:
            self.ticks.update({instr: Tick(instr)})

    def start_loop(self):

        while True:
            # command_b = loads(db.lpop('1:commands')):
            # if command_b:
            #        comand,jsom.loads)
            #     commander(command)

            price_b = self.db.lpop(f'{self.name}:prices')

            if not price_b:
                continue

            price_obj = json.loads(price_b)

            if price_obj['type'] == 'PRICE':
                if price_obj['instrument'] in self.instruments:
                    self.ticks[price_obj['instrument']].start(price_obj)  # todo acync

            if price_obj['type'] == 'HEARTBEAT':
                pass
                # print('HEARTBEAT!!!!!!!!')
                # check_time = datetime.now().timestamp()


if __name__ == "__main__":
    ticker = Ticker("price_1")
    print(ticker.ticks)
    ticker.start_loop()




