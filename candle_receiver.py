from account import Account
from instruments import Instrument
from security import oanda_auth_keys


class CandleReceiver:
    """  Asynchronous API receiver for getting candle data from instruments"""

    def __init__(self, instruments=None):
        if instruments is None:
            self.instruments = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id']).get_instruments_names()
        else:
            self.instruments = instruments
        self.instr_objects = []
        for instrument in self.instruments:
            print('for:', instrument)
            self.instr_objects.append(Instrument(oanda_auth_keys[1], instrument, 'S5'))


if __name__ == "__main__":
    """for checking"""
    cr = CandleReceiver()
    print(cr.instruments)
