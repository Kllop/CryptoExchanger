#api
import asyncio
import aiohttp
#folder
from markets import Binance2P2, BinanceSpot
from proxy.proxyList import proxyListMarketP2PRUB

async def startCommand():
    binance = Binance2P2("Jango", True, 5, proxyListMarketP2PRUB)
    try:
        session_timeout = aiohttp.ClientTimeout(total=None,sock_connect=40,sock_read=40)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            data = await binance.GetBestPrice("TinkoffNew", "RUB", "BTC", "BUY", 1000, 1, session)
            print(data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try :
        asyncio.ensure_future(startCommand())
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()