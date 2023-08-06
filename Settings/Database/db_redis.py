import redis
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

class Redis_DB():

    def __init__(self) -> None:
        self.rc = redis.Redis(host='redis-data', port=6500, decode_responses=True, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')

    def setValueStr(self, key:str, value:str) -> None:
        self.rc.set(key, value=value)

    def setValueMapping(self, key:str, value:dict) -> None:
        self.rc.hset(key, mapping = value)

    def setValueList(self, key:str, value:list) -> None:
        self.rc.rpush(key, value)

    def getValueMapping(self, key:str) -> dict:
        return self.rc.hgetall(key)

    def getValueList(self, key:str) -> list:
        return self.rc.lrange(key, 0, 100)
    
    def getValueStr(self, key:str) -> list:
        return self.rc.get(key)
    
    def removeKey(self, key:str) -> None:
        self.rc.delete(key)
