import redis

class Redis_DB():

    def __init__(self) -> None:
        self.rc = redis.Redis(host='redis-data', port=6379, decode_responses=True, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')

    def setValueMapping(self, key:str, value:dict) -> None:
        self.rc.hset(key, mapping = value)

    def setValueList(self, key:str, value:list) -> None:
        self.rc.rpush(key, value)

    def getValueMapping(self, key:str) -> dict:
        return self.rc.hgetall(key)
    
    def getValueMappingCurrent(self, key:str, name:str) -> str:
        return self.rc.hget(name, key)

    def getValueList(self, key:str) -> list:
        return self.rc.lrange(key, 0, 100)
    
    def removeKey(self, key:str) -> None:
        self.rc.delete(key)

    def removeValueMapping(self, key:str, name:str) -> None:
        self.rc.hdel(name, key)