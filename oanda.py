import requests
import json
import security
from datetime import datetime, timedelta
from time import sleep
from sys import getsizeof
import logging
from databases import ConnectDB
import pytz

EDT = pytz.timezone('America/New_York')
ALA = pytz.timezone('America/Los_Angeles')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create the logging file handler

fh = logging.FileHandler("logs/main.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object

logger.addHandler(fh)
logger.info('Start program')
logger.error('check error')


class Oanda:
    addr = "https://api-fxpractice.oanda.com/v3/"
    db_path = "DB/oanda.sqlite"

    def __init__(self, auth):
        self.conn = ConnectDB(Oanda.db_path)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + auth,
                        # 'Accept-Datetime-Format': 'UNIX',
                        'Accept-Datetime-Format': 'RFC3339'
                        }
        self.accounts = self.get_accounts()['accounts']
        self.accounts_ids = [account['id'] for account in self.accounts]
        print(self.accounts)
        print(self.accounts_ids)

    def rest_get(self, sub_str):
        res = None
        for _ in range(10):
            try:
                res = requests.get(f'{Oanda.addr}{sub_str}', headers=self.headers, timeout=20)
                if res.status_code == 200:  # print('Response OK!')
                    return json.loads(res.text)
                else:
                    logger.error(f'Response ERROR - {res}')
                    sleep(4)
            except requests.exceptions.Timeout:
                logger.error(f'Response TIME OUT ERROR - {res}')
                sleep(4)
            except:
                logger.error(f'Response ERROR - {res}')
                sleep(4)

        return None

    def get_accounts(self):
        return self.rest_get("accounts")

    def get_account_details(self, acc_id):
        r = self.rest_get(f"accounts/{acc_id}")
        print(r)

    @classmethod
    def get_timestamp(cls, date_time):
        date_time, microsec = date_time.rstrip('Z').split('.')
        date_time_obj = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        date_time_obj = date_time_obj.replace(microsecond=int(microsec))
        # print(date_time_obj)
        return datetime.timestamp(date_time_obj)

    @classmethod
    def get_date_time(cls, timestamp):
        dt_obj = datetime.fromtimestamp(timestamp)
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
        # print(r)
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
            r = self.rest_get(f"instruments/{self.name}/candles?count=5000&from={from_time}&{self.price}")
        else:
            r = self.rest_get(f"instruments/{self.name}/candles?from={from_time}&to={to_time}&{self.price}")
        if 'candles' not in r:
            logger.error('Error No candles \n', r)
            return
        self.cache = r['candles']
        return r

    def get_all_candles(self, start_time='1990-09-09T0:20:48.932952Z'):
        print(start_time, 'start_time')
        iter = 0
        while True:
            # Todo count Delay time
            self.get_candles_by_time(start_time)
            if not self.cache:
                print(f'The END. start time: {start_time}')
                logger.info(f'The END. start time: {start_time}')
                last_timestamp = self.conn.select_max(self.name, 'timestamp')
                # print('last_timestamp', last_timestamp)
                return last_timestamp

            iter += 1
            print(iter)
            print(len(self.cache))
            new_time = self.get_date_time(self.get_timestamp(self.cache[-1]['time']) + 5)
            if new_time:
                start_time = new_time
            print(start_time)
            self.set_candles()
            sleep(0.01)        # Delay for API

    def get_last_candles(self):
        max_timestamp = self.conn.select_max(self.name, 'timestamp')
        if max_timestamp is None:
            max_timestamp = 0
        print('max_timestamp in', max_timestamp, Oanda.get_date_time(max_timestamp))
        if max_timestamp:
            return self.get_all_candles(Oanda.get_date_time(max_timestamp))
        else:
            print('base is Empty')
            return self.get_all_candles()

    def set_candles(self):
        candles = []
        for candle in self.cache:
            candles.append({
                'timestamp': int(Oanda.get_timestamp(candle['time'])),
                'high': candle['mid']['h'],
                'low': candle['mid']['l'],
                'open': candle['mid']['o'],
                'close': candle['mid']['c'],
                'volume': candle['volume']
                }
            )
        self.conn.insert_many(self.name, candles)
        self.conn.commit()


if __name__ == "__main__":

    acc = Account(security.auth_key, security.account1_id)
    # acc.get_details()
    acc.get_summary()
    # acc.get_instruments()
    # acc.get_instruments('EUR_USD')
    print(acc.instruments)
    print(len(acc.instruments))

    instr = Instrument(security.auth_key, 'AUD_SGD', 'S5')
    print(security.auth_key)
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
    # candles = instr.get_candles_by_time(instr.get_date_time(datetime.now()))
    # candles = instr.get_candles_by_time("2009-10-06T14:12:45.000000Z")
    # print(candles)
    # print(len(candles))
    sleep(1)
    #instr.set_candles()
    #instr.get_all_candles()
    instr.get_last_candles()
    print(getsizeof(instr.candles))
    print(datetime.now())
    print(datetime.now(ALA))
    print(datetime.now(pytz.utc))
    print(datetime.now(EDT))
    print(datetime.now(EDT).weekday())
    # oanda.get_accounts()
    # print(oanda.accounts)
