import psycopg2, traceback
from psycopg2 import Error

class Postgres_DB():
    
    def __init__(self, user:str, password:str, host:str, port:str, database:str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def __getConnectionAndCursor__(self):
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = self.database)
        except Exception as e:
            return None, None
        try:
            cursor = connection.cursor()
        except Exception as e:
            connection.close()
            return None, None
        return connection, cursor
    
    def __closeConnectionAndCursor__(self, connection, cursor) -> None:
        cursor.close()
        connection.close()

    def CheckTable(self, tableName:str) -> bool:
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT table_name FROM information_schema.tables WHERE table_name = '{0}';".format(tableName.lower())
        data = None
        try:
            cursor.execute(request)
            data = cursor.fetchone()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)
        if data != None:
            return True
        return False
    
    def GetLastOrderID(self) -> int:
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT MAX(orderid) FROM OrdersList;"
        data = None
        try:
            cursor.execute(request)
            data = cursor.fetchone()
            print(data, flush=True)
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)
        if data == None:
            return 0
        return data[0]
    
    def getOrderWithOrderID(self, order_id) -> list:
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT * FROM OrdersList WHERE orderid = {0};".format(order_id)
        data = None
        try:
            cursor.execute(request)
            data = cursor.fetchone()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return []
        self.__closeConnectionAndCursor__(connection, cursor)
        return data

    def GetStructTable(self, tableName:str) -> str:
        request = """SELECT column_name, column_default, data_type 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE table_name = '{0}';""".format(tableName)
        return request

    def createTableUser(self) -> None:
        request = """CREATE TABLE UsersData (login VARCHAR(30) NOT NULL,
                                                       password VARCHAR(256) NOT NULL,
                                                       email VARCHAR(60) NOT NULL,
                                                       datereg VARCHAR(30) NOT NULL,
                                                       datelast VARCHAR(30) NOT NULL,
                                                       ip VARCHAR(30) NOT NULL,
                                                       referal VARCHAR(256) NOT NULL,
                                                       referalcode VARCHAR(256) NOT NULL,
                                                       permision VARCHAR(20) NOT NULL,
                                                       referalpercent FLOAT NOT NULL,
                                                       personalsale FLOAT NOT NULL,
                                                       id VARCHAR(256) NOT NULL);"""
        connection, cursor = self.__getConnectionAndCursor__()
        try:
            cursor.execute(request)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error create direction preference table", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)
    
    def createUser(self, login:str, passowrd:str, email:str, datereg:str, datelast:str, ip:str, referal:str, referal_code:str, permision:str, 
                   referalpercent:str, personal:float, id_code:str) -> None:
        try:
            if not self.CheckTable("UsersData"):
                self.createTableUser()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        try:
            connection, cursor = self.__getConnectionAndCursor__()
            values = [login, passowrd, email, datereg, datelast, ip, referal, referal_code, permision, referalpercent, personal, id_code]
            request = "INSERT INTO UsersData VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(request, values)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error execute request UsersData", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)

    def GetReferalBid(self, referal_code:str) -> tuple:
        try:
            if not self.CheckTable("OrdersList"):
                self.createTableOrdersList()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT * FROM OrdersList WHERE referal = '{0}' AND status = 'payment';".format(referal_code)
        data = []
        try:
            cursor.execute(request)
            data = cursor.fetchall()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return []
        self.__closeConnectionAndCursor__(connection, cursor)
        if data == None:
            return []
        return data
    
    def GetAll_My_Bids(self, code_id:str) -> tuple:
        try:
            if not self.CheckTable("OrdersList"):
                self.createTableOrdersList()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database", flush=True)
            return
        request = "SELECT * FROM OrdersList WHERE owner = '{0}';".format(code_id)
        data = []
        try:
            cursor.execute(request)
            data = cursor.fetchall()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return []
        self.__closeConnectionAndCursor__(connection, cursor)
        if data == None:
            return []
        return data

    def GetFreeUserData(self, login:str, email:str) -> tuple:
        try:
            if not self.CheckTable("UsersData"):
                self.createTableUser()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT * FROM UsersData WHERE login = '{0}' OR email = '{1}';".format(login, email)
        data = []
        try:
            cursor.execute(request)
            data = cursor.fetchall()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return []
        self.__closeConnectionAndCursor__(connection, cursor)
        if data == None:
            return []
        return data
    
    def GetReferalUserData(self, code_id:str) -> tuple:
        try:
            if not self.CheckTable("UsersData"):
                self.createTableUser()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT referal FROM UsersData WHERE id = '{0}';".format(code_id)
        data = []
        try:
            cursor.execute(request)
            data = cursor.fetchone()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return ""
        self.__closeConnectionAndCursor__(connection, cursor)
        if data == None:
            return ""
        return data[0]
    
    def GetReferalCodeUserData(self, code_id:str) -> tuple:
        try:
            if not self.CheckTable("UsersData"):
                self.createTableUser()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT referalcode FROM UsersData WHERE id = '{0}';".format(code_id)
        data = []
        try:
            cursor.execute(request)
            data = cursor.fetchone()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return ""
        self.__closeConnectionAndCursor__(connection, cursor)
        if data == None:
            return ""
        return data[0]

    def GetUserData(self, login:str) -> tuple:
        try:
            if not self.CheckTable("UsersData"):
                self.createTableUser()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database")
            return
        request = "SELECT * FROM UsersData WHERE login = '{0}';".format(login)
        data = None
        try:
            cursor.execute(request)
            data = cursor.fetchone()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error check table", flush=True)
            return []
        self.__closeConnectionAndCursor__(connection, cursor)
        return data

    def createTableDirectionPreference(self) -> None:
        request = """CREATE TABLE DirectionPreference (coin VARCHAR(30) NOT NULL,
                                                       nameexch VARCHAR(30) NOT NULL,
                                                       nameru VARCHAR(30) NOT NULL,
                                                       nameen VARCHAR(30) NOT NULL,
                                                       namedes VARCHAR(30) NOT NULL,
                                                       percent FLOAT NOT NULL,
                                                       marketP2P VARCHAR(10) NOT NULL);"""
        connection, cursor = self.__getConnectionAndCursor__()
        try:
            cursor.execute(request)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error create direction preference table", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)

    def createTableOrdersList(self) -> None:
        request = """CREATE TABLE OrdersList (orderid INT NOT NULL,
                                              datecreate VARCHAR(60) NOT NULL,
                                              datechange VARCHAR(60) NOT NULL,
                                              course VARCHAR(30) NOT NULL,
                                              coin VARCHAR(30) NOT NULL,
                                              price FLOAT NOT NULL,
                                              count FLOAT NOT NULL,
                                              telegram VARCHAR(120) NOT NULL,
                                              paymethod VARCHAR(30) NOT NULL,
                                              paymethodnumber VARCHAR(30) NOT NULL,
                                              wallet VARCHAR(120) NOT NULL,
                                              status VARCHAR(20) NOT NULL,
                                              referal VARCHAR(256) NOT NULL,
                                              owner VARCHAR(256) NOT NULL);"""
        connection, cursor = self.__getConnectionAndCursor__()
        try:
            cursor.execute(request)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error create order list table", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)

    def SendOrder(self, order_id:str, date_create:str, date_change:str, course:str, coin:str, price:float, count:float, 
                  telegram:str, pay_method:str, pay_method_number:str, wallet:str, status:str, referal:str, owner:str) -> None:
        try:
            if not self.CheckTable("OrdersList"):
                self.createTableOrdersList()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return
        try:
            connection, cursor = self.__getConnectionAndCursor__()
            values = [order_id, date_create, date_change, course, coin, price, count, telegram, 
                      pay_method, pay_method_number, wallet, status, referal, owner]
            request = "INSERT INTO OrdersList VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(request, values)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error execute request SendDirectoion", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)

    def ChangeStatusOrder(self, order_id:str, new_status:str) -> bool:
        try:
            if not self.CheckTable("OrdersList"):
                self.createTableDirectionPreference()
        except Exception as e:
            print("Error check table OrdersList", e, traceback.format_exc(), flush=True)
            return False
        try:
            connection, cursor = self.__getConnectionAndCursor__()
            request = "UPDATE OrdersList SET status = '{0}' WHERE orderid = {1};".format(new_status, order_id)
            cursor.execute(request)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error update SendDirectoion", e, traceback.format_exc(), flush=True)
            return False
        self.__closeConnectionAndCursor__(connection, cursor)
        return True

    def SendDirectoion(self, coin:str, name_exch:str, name_ru:str, name_en:str, name_des:str, percent:float, market:str) -> None:
        try:
            if not self.CheckTable("DirectionPreference"):
                self.createTableDirectionPreference()
        except Exception as e:
            print("Error check table SendDirectoion", e, traceback.format_exc(), flush=True)
            return
        try:
            connection, cursor = self.__getConnectionAndCursor__()
            values = [coin, name_exch, name_ru, name_en, name_des, percent, market]
            request = "INSERT INTO DirectionPreference VALUES(%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(request, values)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error execute request SendDirectoion", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)

    def __getDirection__(self, request:str) -> dict:
        connection, cursor = self.__getConnectionAndCursor__()
        if connection == None or cursor == None:
            print("Error connection database", flush=True)
        try:
            cursor.execute(request)
            data = cursor.fetchall()
        except Exception as e:
            print("Error select get direction", e, traceback.format_exc(), flush=True)
            self.__closeConnectionAndCursor__(connection, cursor)
            return []
        self.__closeConnectionAndCursor__(connection, cursor)
        return data

    def GetDirectionWithCoin(self, coin:str) -> None:
        request = """SELECT * FROM DirectionPreference WHERE coin = '{0}'""".format(coin)
        return self.__getDirection__(request)
    
    def GetDirection(self) -> None:
        request = """SELECT * FROM DirectionPreference"""
        return self.__getDirection__(request)
    
    def ClearTable(self, tableName:str) -> None:
        try:
            if not self.CheckTable(tableName):
                self.createTableDirectionPreference()
        except Exception as e:
            print("Error check table {0}".format(tableName), e, traceback.format_exc(), flush=True)
            return     
        try:
            connection, cursor = self.__getConnectionAndCursor__()
            request = "TRUNCATE TABLE {0}".format(tableName)
            cursor.execute(request)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error truncate table SendDirectoion", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)

    def DropTable(self, tableName:str) -> None:
        try:
            connection, cursor = self.__getConnectionAndCursor__()
            request = "DROP TABLE {0}".format(tableName)
            cursor.execute(request)
            connection.commit()
        except Exception as e:
            self.__closeConnectionAndCursor__(connection, cursor)
            print("Error drop table SendDirectoion", e, traceback.format_exc(), flush=True)
        self.__closeConnectionAndCursor__(connection, cursor)