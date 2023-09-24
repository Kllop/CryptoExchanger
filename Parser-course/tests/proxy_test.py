import unittest
import requests

from proxy import Proxy, proxyListMarketP2PRUB

class TestProxy(unittest.TestCase):

    def setUp(self) -> None:
        self.proxy = Proxy(proxyListMarketP2PRUB)
    
    def __check_connection__(self) -> tuple():
        proxy_path = self.proxy.GetProxy()
        responce = requests.get("https://github.com/", proxies={"http" : "http://{0}".format(proxy_path)}, timeout=30)
        return responce.status_code, proxy_path

    def test_proxy_connection(self) -> None:
        for i in range(0, len(proxyListMarketP2PRUB)):
            status_code, proxy_path = self.__check_connection__()
            try:
                self.assertAlmostEqual(status_code, 200)
                status ="OK"
            except:
                status ="FALSE"
            finally:
                print("PROXY : {0} ... {1}".format(proxy_path, status), flush=True)

if __name__ == "__main__":
    unittest.main()