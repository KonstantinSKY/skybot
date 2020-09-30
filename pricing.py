from account import Account
from security import oanda_auth_keys
from logger import Logger

log = Logger(__name__)


class Pricing(Account):

    def __init__(self, auth, acc_id):
        super().__init__(auth, acc_id)
        self.url_pricing = f'{self.url_account}/pricing'
        log.log_info('Pricing Init')

    def pricing(self, instruments):
        instr_str = "%2C".join(instruments)
        print(instr_str)
        return self.get(f'{self.url_pricing}?instruments={instr_str}')

    def stream(self, instruments):
        del self.client.headers['Content-Type']
        print(self.client.headers)
        instr_str = "%2C".join(instruments)
        print(instr_str)
        # return self.get(f'{self.url_pricing}?instruments={instr_str}')


if __name__ == "__main__":
    price = Pricing(oanda_auth_keys[1], '101-001-15249313-001')
    print(price.pricing(['EUR_USD', 'USD_CAD']))
    print(price.stream(['EUR_USD', 'USD_CAD']))
