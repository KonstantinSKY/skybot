from account import Account
from instruments import Instrument
from security import oanda_auth_keys
import asyncio
from oanda_api import OandaAPI
import json
from datetime import datetime
from logger import Logger

log = Logger(__name__)


def main():
    """main loop for getting candles"""
    while True:
        tasks = [cr.loop.create_task(cr.get_last_candles(instr_obj)) for instr_obj in cr.instr_objects]
        start_time = datetime.now().timestamp()
        cr.loop.run_until_complete(asyncio.wait(tasks))
        print("time for :", datetime.now().timestamp() - start_time)


class CandleReceiver(OandaAPI):
    """  Asynchronous API receiver for getting candle data from instruments"""

    def __init__(self, auth, instruments=None):
        """
        API receiver object constructor
        :param instruments: list of str -> list of instruments names
        :var self.instruments: list of str -> list of instruments names
        :var self.instr_objects: list of objects -> objects of instrument list for receiving candle data
        :var self.pause: int, seconds -> pause between requests for one instrument
        """
        super().__init__(auth)
        if instruments is None:
            self.instruments = Account(auth, auth['id']).get_instruments_names()
        else:
            self.instruments = instruments
        self.instr_objects = []

        for instrument in self.instruments:
            self.instr_objects.append(Instrument(auth, instrument, 'S5'))
        self.pause = 5
        self.loop = asyncio.get_event_loop()

    async def get_last_candles(self, instr_obj):
        """ Async Getting  all last candles
        :param instr_obj: object -> instrument object
        :var self.params: dict -> parameters for url request
        """
        print('instr_obj.url_candles', instr_obj.url_candles)
        self.params = instr_obj.params
        if datetime.now().timestamp() - int(float(self.params['from'])) < self.pause:
            # log.prn_log_info(f'Canceled. Pause less then 5 sec. {instr_obj.name}, '
            #                  f'from_time:, {self.params["from"]}, now: {datetime.now().timestamp()}')
            return

        res = await self.get_async(instr_obj.url_candles, timeout=2)
        instr_obj.candle_cache = json.loads(res)['candles'] if res is not None else None

        instr_obj.verify_candles()

        if instr_obj.candle_cache:
            instr_obj.set_candles()


if __name__ == "__main__":
    """for checking"""
    # cr = CandleReceiver(oanda_auth_keys[1])
    cr = CandleReceiver(oanda_auth_keys[1], ["EUR_USD", "USD_CAD", "CHF_HKD", "USD_SEK", "CHF_JPY",
                                             "AUD_NZD", "EUR_GBP", "USD_THB", "EUR_NOK", "AUD_CAD"])
    main()


