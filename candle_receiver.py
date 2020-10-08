from account import Account
from instruments import Instrument
from security import oanda_auth_keys
import asyncio
from time import sleep
from oanda_api import OandaAPI
import json
from datetime import datetime
from logger import Logger

log = Logger(__name__)


class CandleReceiver(OandaAPI):
    """  Asynchronous API receiver for getting candle data from instruments"""

    def __init__(self, auth, instruments=None):
        """
        API receiver object constructor
        :param instruments: list of str -> list of instruments names
        :var self.instruments: list of str -> list of instruments names
        :var self.instr_objects: list of objects -> list objects of instrument for receiving candle data
        """
        super().__init__(auth)
        if instruments is None:
            self.instruments = Account(auth, auth['id']).get_instruments_names()
        else:
            self.instruments = instruments
        self.instr_objects = []

        for instrument in self.instruments:
            self.instr_objects.append(Instrument(auth, instrument, 'S5'))

        self.loop = asyncio.get_event_loop()

    async def get_last_candles(self, instr_obj):
        """ Get all last candles"""
        print('instr_obj.url_candles', instr_obj.url_candles)
        self.params = instr_obj.params
        # await self.__waiter__()
        print('now:', datetime.now().timestamp())
        print('int:', self.params['from'])
        if datetime.now().timestamp() - int(float(self.params['from'])) < 10:
            print('canceled ==========================================>')
            print('now:', datetime.now().timestamp())
            print('int:', self.params['from'])
            return

        res = await self.get_async(instr_obj.url_candles)
        instr_obj.candle_cache = json.loads(res)['candles']
        print('instr_obj.url_candles', instr_obj.url_candles)
        print(len(instr_obj.candle_cache))
        # print(instr_obj.candle_cache[-1])
        instr_obj.verify_candles()
        if instr_obj.candle_cache:
            instr_obj.set_candles()

    async def __waiter__(self):
        log.prn_log_info(f'Waiter: Next start time: {self.params["from"]})')
        log.prn_log_info(f'Now:  {datetime.now().timestamp()} {datetime.now()} ')

        if (datetime.now().timestamp() - int(float(self.params['from']))) < 60:
            check_time = datetime.now().timestamp() // 5 * 5 + 5
            log.prn_log_info(f'NEED TO sleep: {check_time - datetime.now().timestamp()}')
            await asyncio.sleep(check_time - datetime.now().timestamp())


if __name__ == "__main__":
    """for checking"""
    cr = CandleReceiver(oanda_auth_keys[1])
    # print(cr.instruments)
    # print(cr.instr_objects)


    while True:
        tasks = [cr.loop.create_task(cr.get_last_candles(instr_obj)) for instr_obj in cr.instr_objects]
        start_time = datetime.now().timestamp()
        cr.loop.run_until_complete(asyncio.wait(tasks))
        print("time for :", datetime.now().timestamp() - start_time)
        # sleep(10)

    #
    # print('headers', cr.instr_objects[0].headers)
    # print(cr.instr_objects[0].__dict__)
    # main()
