import aiohttp
import asyncio
from aiohttp_requests import requests
from security import auth_key

auth = auth_key

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer', ,
          'Accept-Datetime-Format': 'UNIX'
          }


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())


# session = aiohttp.ClientSession()
# headers = {'Accept - Encoding': 'gzip, deflate',
#                                'Content-Type': 'application/json',
#                                'Authorization': 'Bearer ' + auth_key,
#                                'Accept-Datetime-Format': 'UNIX'}
#
#
# async with session.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5') as r:
#     print(r.headers)
#     print(await r.text())


# await session.close()
#
#
# client = requests.session
# client.
#
#
# async def main():
#     pass

if __name__ == '__main__':
    help(requests)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
