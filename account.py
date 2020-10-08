from oanda_api import OandaAPI
from security import oanda_auth_keys
from logger import Logger

log = Logger(__name__)


class Account(OandaAPI):
#TODO
    def __init__(self, auth, acc_id):
        super().__init__(auth)
        if acc_id not in self.accounts_ids:
            raise Exception(f"Account {acc_id} not exist for this Oanda key!")
        self.url_account = f'{self.url_accounts}/{acc_id}'
        self.instruments = []
        log.log_info('Account Init')

    def get_details(self):
        return self.get(self.url_account)

    def get_summary(self):
        return self.get(f'{self.url_account}/summary')

    def get_instruments(self, name=None):
        if name is None:
            return self.get(f'{self.url_account}/instruments')['instruments']
        return self.get(f'{self.url_account}/instruments?instruments={name}')['instruments']

    def get_instruments_names(self):
        return [instr['name'] for instr in self.get_instruments()]
    #
    # def get_latest_candles(self):
    #     return self.get(f"{self.url_account}/candles/latest")

if __name__ == "__main__":
    acc = Account(oanda_auth_keys[1], '101-001-15249313-001')
    print(acc.accounts_ids)
    print(acc.url_accounts)
    print(acc.url_account)
    print(acc.get_details())
    print(acc.get_summary())
    names = acc.get_instruments_names()

    print(acc.get_instruments())
    print(names)
    # print(acc.get_instruments('EUR_USD'))
    # print(acc.get_latest_candles())
