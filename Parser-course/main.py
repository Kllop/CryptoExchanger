#api
import asyncio
import aiohttp
import json
#folder
from Database.db_redis import Redis_DB
from markets import BinanceSpot, ByBit2P2
from proxy.proxyList import proxyListMarketP2PRUB

redis_db = Redis_DB()

async def ByBitP2PCourse(preference) -> int:
    try:
        bybit = ByBit2P2("", True, 5, proxyListMarketP2PRUB)
        session_timeout = aiohttp.ClientTimeout(total=None,sock_connect=40,sock_read=40)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            return await bybit.GetBestPrice(preference["name_exch"], "RUB", preference["coin"], "BUY", session)        
    except ConnectionError as e:
        print("Error connection ByBit P2P", flush=True)
        return 0
    except Exception as e:
        print(e, flush=True)
        return 0

async def setCourseData(coin:str, data):
    redis_db.setValueMapping("courses", {coin : data})

async def masterMarket():
    preferences = await parse_preference(redis_db.getValueList("tradepreference"))
    print(preferences, flush=True)
    directionMarket = await WorkManager(preferences)
    print(directionMarket, flush=True)
    outdata = {}
    for direction in directionMarket:
        market : str = direction['market']
        area : str = direction['area']
        coin : str = direction['coin']
        data = 0
        if market == "bybit":
            if area == "p2p":
                data = await ByBitP2PCourse(direction)
                print(data, flush=True)
        outdata.update({"{0}:{1}:{2}:{3}".format(market, area, coin, direction["name_exch"]) : data})
    redis_db.removeKey("courses")
    for preference in preferences:
        price = outdata.get("{0}:{1}:{2}:{3}".format(preference["market"], preference["area"], preference["coin"], preference["name_exch"]))
        if price == 0:
            continue
        price = round(price * ((100 + preference.get("percent"))/100), 2)
        await setCourseData("{0}:{1}".format(preference["coin"], preference["name_des"]), price)

async def WorkManager(preference):
    outdata = []
    for data in preference:
        outdata.append({"market" : data['market'], "area" : data['area'], "coin" : data['coin'], "name_exch" : data['name_exch']})
    outdata = [i for n, i in enumerate(outdata) if i not in outdata[:n]]
    return outdata

async def start():
    while True:
        await masterMarket()
        print("start", flush=True)
        await asyncio.sleep(15)

async def parse_preference(data:dict) -> dict:
    outdata = []
    for temp in data:
        outdata.append(json.loads(temp))
    return outdata

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try :
        asyncio.ensure_future(start())
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()