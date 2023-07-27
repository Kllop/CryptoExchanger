#api
import asyncio
import aiohttp
import json
#folder
from Database.db_redis import Redis_DB
from markets import Binance2P2, BinanceSpot
from proxy.proxyList import proxyListMarketP2PRUB

redis_db = Redis_DB()

async def BinanceCourse(preferences):
    try:
        binance = Binance2P2("", False, 5, proxyListMarketP2PRUB)
        session_timeout = aiohttp.ClientTimeout(total=None,sock_connect=40,sock_read=40)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            for preference in preferences:
                if preference["market"] == "P2P":
                    data = await binance.GetBestPrice(preference["name_exch"], "RUB", preference["coin"], "BUY", 1000, 1, session)
                elif preference["market"] == "SPOT":
                    data = BinanceSpot()
                else:
                    data = {}
                redis_db.setValueMapping("binancecourse", {preference["coin"] : json.dumps(data)})
    except ConnectionError as e:
        print("Error connection", flush=True)
    except Exception as e:
        print(e, flush=True)

async def start():
    while True:
        preference = parse_preference(redis_db.getValueList("tradepreference"))
        await BinanceCourse(preference)
        print(redis_db.getValueMapping("binancecourse",), flush=True)
        await asyncio.sleep(15)

def parse_preference(data:dict) -> dict:
    outdata = []
    for temp in data:
        outdata.append(json.loads(temp))
    return outdata

if __name__ == "__main__":
    redis_db.removeKey("binancecourse")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try :
        asyncio.ensure_future(start())
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()