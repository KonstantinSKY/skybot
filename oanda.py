import requests
import json
import security


class Oanda:

    def __init__(self, auth):
        self.addr = "https://api-fxpractice.oanda.com/v3/"
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + auth}
        self.accounts = self.get_accounts()['accounts']
        self.accounts_ids = [account['id'] for account in self.accounts]
        print(self.accounts)
        print(self.accounts_ids)

    def rest_get(self, sub_str):
        res = requests.get(f'{self.addr}{sub_str}', headers=self.headers)
        return json.loads(res.text)

    def get_accounts(self):
        return self.rest_get("accounts")

    def get_account_details(self, acc_id):
        r = self.rest_get(f"accounts/{acc_id}")
        print(r)


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
        self.cache = {}

    def get_last_candles_by_count(self, count):
        if count > 5000:
            count = 5000
        r = self.rest_get(f"instruments/{self.name}/candles?count={count}&price=M&granularity={self.granularity}")['candles']
        self.cache = r
        print(r)
        print(len(r))
        return r

    def get_last_candles_by_time(self, granularity):
        pass


acc = Account(security.auth_key, security.account1_id)

# acc.get_details()
acc.get_summary()
# acc.get_instruments()
# acc.get_instruments('EUR_USD')
print(acc.instruments)
print(len(acc.instruments))

instr = Instrument(security.auth_key, 'EUR_USD', 'S5')
instr.get_last_candles_by_count(5001)


#oanda.get_accounts()
# print(oanda.accounts)
