import requests
import json
import security
from datetime import datetime, timedelta
from time import sleep
from sys import getsizeof


class Oanda:
    addr = "https://api-fxpractice.oanda.com/v3/"

    def __init__(self, auth):
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + auth}
        self.accounts = self.get_accounts()['accounts']
        self.accounts_ids = [account['id'] for account in self.accounts]
        print(self.accounts)
        print(self.accounts_ids)

    def rest_get(self, sub_str):
        res = requests.get(f'{Oanda.addr}{sub_str}', headers=self.headers)
        return json.loads(res.text)

    def get_accounts(self):
        return self.rest_get("accounts")

    def get_account_details(self, acc_id):
        r = self.rest_get(f"accounts/{acc_id}")
        print(r)

    @classmethod
    def get_time_obj(cls, date_time):
        date_time, microsec = date_time.rstrip('Z').split('.')
        date_time_obj = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        date_time_obj = date_time_obj.replace(microsecond=int(microsec))
        # print(date_time_obj)
        return date_time_obj

    @classmethod
    def get_date_time(cls, dt_obj):
        month = str(dt_obj.month).zfill(2)
        day = str(dt_obj.day).zfill(2)
        hour = str(dt_obj.hour).zfill(2)
        minute = str(dt_obj.minute).zfill(2)
        second = str(dt_obj.second).zfill(2)
        microsecond = str(dt_obj.microsecond).zfill(6)
        return f'{dt_obj.year}-{month}-{day}T{hour}:{minute}:{second}.{microsecond}Z'


class Account(Oanda):

    def __init__(self, auth, acc_id):
        super().__init__(auth)
        if acc_id in self.accounts_ids:
            self.acc_id = acc_id
        else:
            self.acc_id = None
            print(f"Account {acc_id} not exist ")
        self.instruments = []

    def get_details(self):
        r = self.rest_get(f"accounts/{self.acc_id}")
        print(r)
        return r

    def get_summary(self):
        r = self.rest_get(f"accounts/{self.acc_id}/summary")
        print(r)
        return r

    def get_instruments(self, name=None):
        if name is None:
            r = self.rest_get(f"accounts/{self.acc_id}/instruments")['instruments']
            self.instruments = [instrument['name'] for instrument in r]
        else:
            r = self.rest_get(f"accounts/{self.acc_id}/instruments?instruments={name}")['instruments']
        print(r)
        return r


class Instrument(Oanda):

    def __init__(self, auth, name, granularity):
        super().__init__(auth)
        self.name = name
        self.granularity = granularity
        self.price = f'price=M&granularity={self.granularity}'
        self.cache = {}
        self.candles = {}

    def get_last_candles_by_count(self, count):
        if count > 5000:
            count = 5000
        r = self.rest_get(f"instruments/{self.name}/candles?count={count}&{self.price}")['candles']
        self.cache = r
        return r

    def get_candles_by_time(self, from_time, to_time=None):
        if to_time is None:
            r = self.rest_get(f"instruments/{self.name}/candles?count=5000&from={from_time}&{self.price}")['candles']
        else:
            r = self.rest_get(f"instruments/{self.name}/candles?from={from_time}&to={to_time}&{self.price}")['candles']
        self.cache = r
        return r

    def get_all_candles(self):
        start_time = '1990-09-09T0:20:48.932952Z'
        iter = 0
        while True:
            self.get_candles_by_time(start_time)
            if not self.cache:
                print('The END')
                break
            iter += 1
            print(iter)
            print(len(self.cache))
            start_time = self.get_date_time(self.get_time_obj(self.cache[-1]['time']) + timedelta(seconds=5))
            # start_time = self.cache[-1]['time']
            print(start_time)
            self.set_candles()
            print("len", len(self.candles))
            print("getsizeof", getsizeof(self.candles))
            sleep(3)

    def set_candles(self):
        for candle in self.cache:
            self.candles.update({datetime.timestamp(Oanda.get_time_obj(candle['time'])): {
                'open': candle['mid']['o'],
                'close': candle['mid']['c'],
                'high': candle['mid']['h'],
                'low': candle['mid']['l'],
                'volume': candle['volume']
                }
            })
            # print(self.candles)

            # print(len(self.candles))
            #sleep(1)


acc = Account(security.auth_key, security.account1_id)
# acc.get_details()
acc.get_summary()
# acc.get_instruments()
# acc.get_instruments('EUR_USD')
print(acc.instruments)
print(len(acc.instruments))

instr = Instrument(security.auth_key, 'EUR_USD', 'S5')
# instr.get_last_candles_by_count(5001)
time = datetime.now()

# print(time)
# print(time.date())
# print(time.time())
# print(f'{time.date()}T{time.time()}Z')
# print(datetime.timestamp(time))
# print(datetime.timestamp(time)+5)
# dt_obj1 = Oanda.get_time_obj('2020-09-09T22:00:48.932952Z')
# print(datetime.timestamp(dt_obj1))
# print(Oanda.get_date_time(dt_obj1))
# candles = instr.get_candles_by_time('2020-09-09T20:20:48.932952Z', Oanda.get_date_time(datetime.now()))
candles = instr.get_candles_by_time('2020-09-09T0:20:48.932952Z')
print(candles)
print(len(candles))
#instr.set_candles()
instr.get_all_candles()
print(getsizeof(instr.candles))
# oanda.get_accounts()
# print(oanda.accounts)
