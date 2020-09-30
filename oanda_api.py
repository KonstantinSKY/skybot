from rest_api import RestAPI
import security
from logger import Logger
from databases import ConnectDB
from security import oanda_auth_keys
from datetime import datetime
import pytz

log = Logger(__name__)

TRADE_ENV = {
    "practice": {
        "stream": 'https://stream-fxpractice.oanda.com/v3/',
        "api": 'https://api-fxpractice.oanda.com/v3/'
    },
    "live": {
        "stream": 'https://stream-fxtrade.oanda.com/v3/',
        "api": 'https://api-fxtrade.oanda.com/v3/'
    }
}


class OandaAPI(RestAPI):
    db_path = "DB/oanda.sqlite"
    EDT = pytz.timezone('America/New_York')
    ALA = pytz.timezone('America/Los_Angeles')

    def __init__(self, auth):
        super().__init__()
        self.conn = ConnectDB(OandaAPI.db_path)

        if TRADE_ENV[auth['env']]:
            self.url_api = TRADE_ENV[auth['env']]['api']
            self.url_stream = TRADE_ENV[auth['env']]['stream']
        else:
            log_rest.log_err(f"Unknown trade environment: {auth['env']}")

        self.client.headers = {'Accept - Encoding': 'gzip, deflate',
                               'Content-Type': 'application/json',
                               'Authorization': 'Bearer ' + auth['key'],
                               'Accept-Datetime-Format': 'UNIX',
                               }
        self.url_accounts = f"{self.url_api}accounts"
        self.accounts_ids = [account['id'] for account in self.get_accounts()['accounts']]  # accounts ids list
        log.log_info('Oanda_API Init')

    def get_accounts(self):
        return self.get(self.url_accounts)

    @staticmethod
    def from_ts(timestamp):
        return datetime.fromtimestamp(float(timestamp))


if __name__ == "__main__":
    oanda = OandaAPI(oanda_auth_keys[1])
    # print(oanda.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5').text)
    # print(oanda.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5&alignmentTimezone=GMT').text)
    # print(oanda.get('https://api-fxpractice.oanda.com/v3/accounts').text)
    print(oanda.get('https://api-fxpractice.oanda.com/v3/accounts'))
    print(oanda.get_accounts())
    print(oanda.accounts_ids)
    # print(oanda.get_account_details('101-001-15249313-002'))
    # print(oanda.get_account_summary('101-001-15249313-001'))
