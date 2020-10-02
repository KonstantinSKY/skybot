import aiohttp
import asyncio
from aiohttp_requests import requests
from security import auth_key

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


# session = aiohttp.ClientSession()
# headers = {'Accept - Encoding': 'gzip, deflate',
#                                'Content-Type': 'application/json',
#                                'Authorization': 'Bearer ' + auth_key,
#                                'Accept-Datetime-Format': 'UNIX'}
#
# async with session.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5') as r:
#     print(r.headers)
#     print(await r.text())


# session.close()
#
#
# client = requests.session
# client.
#
#
# async def main():
#     pass

if __name__ == '__main__':
    # help(requests)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main(1, 'EUR_USD'), main(2, 'AUD_CHF'), main(3, 'EUR_CHF')))
