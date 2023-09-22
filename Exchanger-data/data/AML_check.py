import aiohttp
import asyncio
import json
import random

class AML:

    url = "https://api.getblock.net/rpc/v1/request"
    headers = {"Authorization" : "Bearer HcLDUcmWjgdujPQb3Kx6-yMh_4zLmKZjmZQuy_K9"}
    _network = {"BTC" : "BTC", "ETH" : "ETH", "USDT_TRC20" : "TRX"}

    async def __check__(self, wallet:str, network:str, id_transaktion:str) -> None:
        data = {"jsonrpc":"2.0", "id": id_transaktion, "method":"checkup.checkaddr", "params":{ "addr":wallet, "currency": network}}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url, data=json.dumps(data)) as resp:
                jsdata = await resp.json()
                resualt = jsdata.get("result")
                if resualt == None:
                    return None
                check = resualt.get("check")
                if check == None:
                    return None
                return check.get("hash")

    async def __get_info__(self, hash_info:str, id_transaktion:str) -> None:
        data = { "jsonrpc":"2.0","id": id_transaktion,"method":"checkup.getresult", "params":{"hash": hash_info}}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url, data=json.dumps(data)) as resp:
                jsdata = await resp.json()
                resualt = jsdata.get("result")
                if resualt == None or len(resualt) == 0:
                    return None
                check = resualt.get("check")
                if resualt == None or len(resualt) == 0:
                    return check
                report = check.get("report")
                if report == None or len(report) == 0:
                    return None
                score = report.get("riskscore")
                if score == None:
                    return 0
                return score

    async def check_wellet(self, wallet:str, coin:str) -> None:
        network = self._network.get(coin)
        if network == None:
            return None
        id_transaktion = random.randint(1000000, 9999999)
        hash_info = await self.__check__(wallet, network, id_transaktion)
        if hash_info == None:
            return None
        await asyncio.sleep(20)
        resualt = await self.__get_info__(hash_info, id_transaktion)
        return resualt



print(asyncio.run(AML().check_wellet("TFg4UkteDnJWCnjo1vZ1nB73anUjfDaDSm", "USDT_TRC20")))