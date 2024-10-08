class Proxy:

    def __init__(self, proxyList:list[str]) -> None:
        if len(proxyList) == 0:
            raise(Exception("Error empty proxy list"))
        self._currentProxyIndex = -1
        self._proxyList = proxyList

    def _NextProxy(self) -> str:
        self._currentProxyIndex = (self._currentProxyIndex + 1) % len(self._proxyList) 

    def GetProxy(self) -> str:
        self._NextProxy()
        return self._proxyList[self._currentProxyIndex]