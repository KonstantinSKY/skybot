import aiohttp
import asyncio
from aiohttp_requests import requests
from security import auth_key
from datetime import datetime

auth = f'Bearer {auth_key}'

headers = {'Content-Type': 'application/json',
           'Authorization': auth,
           'Accept-Datetime-Format': 'UNIX'
           }

params = [('count', '6'), ('price', 'M'), ('granularity', 'S5')]


async def main(num, instr):
    print(f'request {num} megasuperstart')

    async with aiohttp.ClientSession() as session:
        print(f'request {num} superstart')
        async with session.get(f'https://api-fxpractice.oanda.com/v3/instruments/{instr}/candles',
                                     headers=headers, params=params) as resp:
            print(f'request {num} start')
            print(resp.status)
            print(await resp.text())
            print(f'request {num} finished')



# session.close()

start_time = datetime.now().timestamp()
if __name__ == '__main__':
    # help(requests)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main(1, 'EUR_USD'), main(2, 'AUD_CHF'), main(3, 'EUR_CHF'),
                                           main(4, 'EUR_TRY'), main(5, 'AUD_HKD'), main(6, 'EUR_NZD')))
    #loop.run_until_complete(asyncio.gather(main(1, 'EUR_USD'), main(2, 'AUD_CHF'), main(3, 'EUR_CHF')))

print('all time:', datetime.now().timestamp()-start_time)
    # async main(5, 'SGD_JPY')
