import requests
import json
import security


class Oanda:

    def __init__(self, auth):
        self.addr = "https://api-fxpractice.oanda.com/v3/"
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + auth}
        self.accounts = {}

    def get_accounts(self):
        r = requests.get(self.addr + "accounts", headers=self.headers)
        print(r.text)
        self.accounts = json.loads(r.text)


oanda = Oanda(security.auth_key)
oanda.get_accounts()
print(oanda.accounts)

