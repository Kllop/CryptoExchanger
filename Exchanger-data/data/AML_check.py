import aiohttp
import asyncio
import json

class AML:

    url = "https://api.getblock.net/rpc/v1/request"
    headers = {"Authorization" : "Bearer HcLDUcmWjgdujPQb3Kx6-yMh_4zLmKZjmZQuy_K9"}
    network = {"BTC" : "BTC", "ETH" : "ETH", "USDT_TRC20" : "TRX"}

    async def __check__(self, wallet:str, network:str, id_transaktion:str) -> None:
        data = {"jsonrpc":"2.0", "id": id_transaktion, "method":"checkup.checkaddr", "params":{ "addr":wallet, "currency": network}}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url, data=json.dumps(data)) as resp:
                print(resp.status)
                print(await resp.text())



asyncio.run(AML().check(2312))