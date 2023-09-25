from Database.db_redis import Redis_DB
import uuid
import json

class DirectionBanks:

    def __init__(self) -> None:
        self.redis_db = Redis_DB()
        self.db_name = "directionbanks"

    def __getUID__(self) -> str:
        return uuid.uuid4().hex

    def __dumps__(self, data:dict) -> dict:
        outdata = {}
        for temp in data:
            outdata.update({temp : json.dumps(data[temp])})
        return outdata

    def __loads__(self, data:dict) -> dict:
        outdata = {}
        for temp in data:
            outdata.update({temp : json.loads(data[temp])})
        return outdata

    def createNewBank(self, bank_ind:str, bank_ru:str, bank_en:str, bank_number:str, bank_owner:str) -> None:
        data = self.getAllBanks()
        set_data = {"bank_ind" : bank_ind, "bank_ru" : bank_ru, "bank_en" : bank_en, "bank_number" : bank_number, "bank_owner" : bank_owner}
        data.update({bank_ind : set_data})
        data = self.__dumps__(data)
        self.redis_db.setValueMapping(self.db_name, data)

    def getAllBanks(self) -> dict:
        data = self.redis_db.getValueMapping(self.db_name)
        if data == None:
            return {}
        return self.__loads__(data)

    def removeBank(self, uid:str) -> None:
        self.redis_db.removeValueMapping(uid, self.db_name)

    def changeBank(self, uid:str, bank_data:dict) -> None:
        data = self.getAllBanks()
        data.update({uid : bank_data})
        data = self.__dumps__(data)
        self.redis_db.setValueMapping(self.db_name, data)