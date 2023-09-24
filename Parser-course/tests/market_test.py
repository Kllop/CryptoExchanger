import aiohttp
import asyncio

from markets import ByBit2P2

class TestBybit():

    sucssess_test = 0
    fail_test = 0

    def __init__(self) -> None:
        self.bybit = ByBit2P2()
        self.market_bybit_dict = {"Raiffeisen" : "64", "Sberbank" : "582", "Tinkoff" : "581"}

    def test_bybit_main(self) -> None:
        print("----------------------------------------------------------------------", flush=True)
        asyncio.run(self.test_bybit_market())
        print("----------------------------------------------------------------------", flush=True)
        print("SUCSSESS : \033[92m {0}\033[00m\tFIAL : \033[91m {1}\033[00m".format(self.sucssess_test, self.fail_test), flush=True)
        assert self.fail_test <= 0  

    async def test_bybit_market(self) -> None:
        price = 0
        session_timeout = aiohttp.ClientTimeout(total=None,sock_connect=40,sock_read=40)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            for pay_method in self.market_bybit_dict:
                try:
                    price = await self.bybit.GetBestPrice(self.market_bybit_dict.get(pay_method), "RUB", "BTC", "BUY", session)
                    assert price != 0
                    status ="\033[92m OK \033[00m"
                    self.sucssess_test += 1
                except:
                    status ="\033[91m FALSE \033[00m"
                    self.fail_test += 1
                finally:
                    print("Connection ByBit : {0} ... {1}".format(pay_method, status), flush=True)

if __name__ == "__main__":
    pass