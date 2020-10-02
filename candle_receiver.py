from account import Account
from instruments import Instrument
from security import oanda_auth_keys
import asyncio
from time import sleep


class CandleReceiver:
    """  Asynchronous API receiver for getting candle data from instruments"""

    def __init__(self, instruments=None):
        """
        API receiver object constructor
        :param instruments: list of str -> list of instruments names
        :var self.instruments: list of str -> list of instruments names
        :var self.instr_objects: list of objects -> list objects of instrument for receiving candle data
        """
        if instruments is None:
            self.instruments = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id']).get_instruments_names()
        else:
            self.instruments = instruments
        self.instr_objects = []

        for instrument in self.instruments:
            self.instr_objects.append(Instrument(oanda_auth_keys[1], instrument, 'S5'))

        self.loop = asyncio.get_event_loop()


# async def get_last(obj):
#     print('object', obj)
#     await obj.get_all_candles()
#

def main():
    loop = asyncio.get_event_loop()
    task_list = [loop.create_task(obj.get_last_candles()) for obj in cr.instr_objects]
    print(task_list)
    loop.run_until_complete(asyncio.wait(task_list))
    pass


if __name__ == "__main__":
    """for checking"""
    cr = CandleReceiver()
    print(cr.instruments)

    main()
