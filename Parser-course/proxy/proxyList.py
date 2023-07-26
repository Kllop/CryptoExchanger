#RUB
loginRUB = "eqAPee"
passwordRUB = "2NdYLw"
proxyListMarketP2PRUB = ["{0}:{1}@185.126.67.44:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.126.67.210:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@45.86.14.247:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@45.86.14.50:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.99.99.253:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.99.98.171:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.99.98.64:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.99.99.220:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.126.67.109:8000".format(loginRUB, passwordRUB),
                      "{0}:{1}@185.126.67.9:8000".format(loginRUB, passwordRUB)]
#USD
loginUSD = "wMyoGx"
passwordUSD = "qTWpMV"
proxyListMarketP2PUSD = ["{0}:{1}@168.80.83.192:8000".format(loginUSD, passwordUSD),
                      "{0}:{1}@168.80.83.175:8000".format(loginUSD, passwordUSD)]

#GEL
loginGEL = "wMyoGx"
passwordGEL = "qTWpMV"
proxyListMarketP2PGEL = ["{0}:{1}@168.80.83.2:8000".format(loginGEL, passwordGEL),
                      "{0}:{1}@168.80.82.101:8000".format(loginGEL, passwordGEL)]

#KZT
loginKZT = "wMyoGx"
passwordKZT = "qTWpMV"
proxyListMarketP2PKZT = ["{0}:{1}@168.80.82.87:8000".format(loginKZT, passwordKZT),
                      "{0}:{1}@168.80.80.133:8000".format(loginKZT, passwordKZT),
                      "{0}:{1}@168.80.82.227:8000".format(loginKZT, passwordKZT)]

proxyListSpot = ['{0}:{1}@168.81.66.79:8000'.format("FMYCab", "RX0jHK")]

if __name__ == '__main__':
    print(len(proxyListMarketP2PRUB))