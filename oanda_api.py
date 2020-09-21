from rest_api import RestAPI
import security
import logger
import json
from databases import ConnectDB

log = logger.log(__name__)

TRADE_ENV = {
    "practice": {
        "stream": 'https://stream-fxpractice.oanda.com',
        "api": 'https://api-fxpractice.oanda.com/v3/'
    },
    "live": {
        "stream": 'https://stream-fxtrade.oanda.com',
        "api": 'https://api-fxtrade.oanda.com/v3/'
    }
}


class Oanda(RestAPI):
    addr = "https://api-fxpractice.oanda.com/v3/"
    db_path = "DB/oanda.sqlite"

    def __init__(self, auth):
        super().__init__()
        self.conn = ConnectDB(Oanda.db_path)
        self.client.headers = {'Content-Type': 'application/json',
                               'Accept - Encoding': 'gzip, deflate',
                               'Authorization': 'Bearer ' + auth,
                               'Accept-Datetime-Format': 'UNIX',
                               }

        self.api = TRADE_ENV['practice']['api']
        self.stream = TRADE_ENV['practice']['stream']
        # self.suffix =

    def set_trade_env(self, env):
        if TRADE_ENV[env]:
            self.api = TRADE_ENV[env]['api']
            self.stream = TRADE_ENV[env]['stream']
        else:
            log.error(f"Unknown trade environment: {env}")

    def get_accounts(self, sub_url=''):
        response = self.get(f'{self.api}accounts/{sub_url}')
        if hasattr(response, 'text'):
            return json.loads(response.text)

    def get_account_details(self, acc_id):
        return self.get_accounts(acc_id)

    def get_account_summary(self, acc_id):
        return self.get_accounts(f'{acc_id}/summary')


if __name__ == "__main__":
    oanda = Oanda(security.auth_key)
    print(oanda.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5').text)
    print(oanda.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5&alignmentTimezone=GMT').text)
    print(oanda.get('https://api-fxpractice.oanda.com/v3/accounts').text)
    # print(oanda.get_accounts())
    print(oanda.get_account_details('101-001-15249313-002'))
    print(oanda.get_account_summary('101-001-15249313-001'))
