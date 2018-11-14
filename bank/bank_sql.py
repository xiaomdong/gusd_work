import sqlite3
import datetime
from enum import Enum
import control

BANK_SQL_DB = "bank.db"
BALANCE_TABLE = "balance"
RECORD_TABLE = "record"

SQL_SEARCH_BALANCE_TABLE = "select * from sqlite_master where type = 'table' and name = '%s'" % (BALANCE_TABLE)
SQL_SEARCH_RECORD_TABLE = "select * from sqlite_master where type = 'table' and name = '%s'" % (RECORD_TABLE)
SQL_CREATE_BALANCE_TABLE = "create table %s (account text primary key, balance integer)" % (BALANCE_TABLE)
SQL_CREATE_RECORD_TABLE = "create table %s (account text, time  text, operation integer, otherAccount text, value integer,recordIndex integer primary key)" % (
    RECORD_TABLE)

SQL_INSERT_BALANCE_TABLE = "insert into %s values (?,?)" % (BALANCE_TABLE)
SQL_SELECT_BALANCE_TABLE = "select * from %s where account=?" % (BALANCE_TABLE)
SQL_UPDATE_BALANCE_TABLE = "update %s set balance=? where account=?" % (BALANCE_TABLE)

SQL_INSERT_RECORD_TABLE = "insert into %s values (?,?,?,?,?,?)" % (RECORD_TABLE)
SQL_SELECT_RECORD_TABLE = "select * from %s where account=? or otherAccount=?" % (RECORD_TABLE)
SQL_SELECT_ALL_RECORD_TABLE = "select * from %s " % (RECORD_TABLE)

CREATE_OPERATION = 0
DEPOSIT_OPERATION = 1
WITHDRAWAL_OPERATION = 2
TRANSER_OPERATION = 3


operation = Enum('operation', ('deposit', 'withdrawal', 'transfer'))

class bankSql():
    def __init__(self, db_path=BANK_SQL_DB):
        self.path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.path,check_same_thread=False)
        # self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

        self.cursor.execute(SQL_SEARCH_BALANCE_TABLE)
        result = self.cursor.fetchall();
        if (len(result) == 0):
            self.cursor.execute(SQL_CREATE_BALANCE_TABLE)
            self.conn.commit()
            print("SQL_CREATE_BALANCE_TABLE ")
        else:
            print("exist %s table" % (BALANCE_TABLE))

        self.cursor.execute(SQL_SEARCH_RECORD_TABLE)
        result = self.cursor.fetchall();
        if (len(result) == 0):
            self.cursor.execute(SQL_CREATE_RECORD_TABLE)
            self.conn.commit()
            print("SQL_CREATE_RECORD_TABLE ")
        else:
            print("exist %s table" % (RECORD_TABLE))


    def runSqlwithCommit(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            return []   #表示执行正常
        except Exception as e:
            self.conn.rollback() # 回滚？
            print("something err:%s" % (e))
            return None #表示执行异常

    def runSqlWithoutCommit(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            result = self.cursor.fetchall();
            return []     #表示执行正常
        except Exception as e:
            self.conn.rollback()  # 回滚？
            print("something err:%s" % (e))
            return None   #表示执行异常

    def runSql(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            result = self.cursor.fetchall();
            if result == None:
                return [] #[]表示表格中没有数据
            return result #表格中有数据
        except Exception as e:
            self.conn.rollback()  # 回滚？
            print("something err:%s" % (e))
            return None   #表示执行异常

    def runSqlWithoutData(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall();
            if result == None:
                return [] #[]表示表格中没有数据
            return result #表格中有数据
        except Exception as e:
            self.conn.rollback()  # 回滚？
            print("something err:%s" % (e))
            return None   #表示执行异常

    def insertBalanceWithoutCommit(self, account, value):
        tmp = (account, value)
        return self.runSqlWithoutCommit(SQL_INSERT_BALANCE_TABLE, tmp)

    def insertBalance(self, account, value):
        tmp = (account, value)
        return self.runSqlwithCommit(SQL_INSERT_BALANCE_TABLE, tmp)

    def updateBalanceWithoutCommit(self, account, value):
        tmp = (value,account)
        return self.runSqlWithoutCommit(SQL_UPDATE_BALANCE_TABLE, tmp)

    def updateBalance(self, account, value):
        tmp = (value,account)
        return self.runSqlwithCommit(SQL_UPDATE_BALANCE_TABLE, tmp)

    def getBalance(self, account):
        tmp = (account,)
        return self.runSql(SQL_SELECT_BALANCE_TABLE, tmp)

    def insertRecord(self, account, time, operation, otherAccount, value, recordIndex):
        tmp = (account, time, operation, otherAccount, value, recordIndex)
        # print(tmp)
        result = self.runSqlwithCommit(SQL_INSERT_RECORD_TABLE, tmp)
        if(result != None):
            control.bankInfo(account, time, operation, otherAccount, value, recordIndex)
        return result

    def getRecord(self, account):
        tmp = (account,account)
        return self.runSql(SQL_SELECT_RECORD_TABLE, tmp)

    def getRecordIndex(self):
        result = self.runSqlWithoutData(SQL_SELECT_ALL_RECORD_TABLE)
        return len(result)

    def close(self):
        self.cursor.close()
        self.conn.close()

# 没有考虑溢出的情况
class bank():
    def __init__(self, db_path=BANK_SQL_DB):
        self.sql = bankSql(db_path)

    def run(self):
        self.sql.connect()

    def exit(self):
        self.sql.close()

    def getBalance(self,account):
        result = self.sql.getBalance(account)
        if(result == None):
            # sql 操作失败，这里暂时都不处理
            return None

        if (result == []):
            return 0
        else:
            return result[0][1]

    # 存款
    def deposit(self, account, value):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        result = self.sql.getBalance(account)
        if(result == None):
            # sql 操作失败，这里暂时都不处理
            return None

        if (result == []):
            self.sql.insertBalanceWithoutCommit(account, value)
            operation = CREATE_OPERATION
            otherAccount = 0
            recordIndex = self.sql.getRecordIndex() + 1
            self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex)
        else:
            _value = result[0][1] + value
            self.sql.updateBalanceWithoutCommit(account, _value)
            operation = WITHDRAWAL_OPERATION
            otherAccount = 0
            recordIndex = self.sql.getRecordIndex() + 1
            self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex)

    # 提现
    def withdrawal(self, account, value):
        if(value==0):
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        result = self.sql.getBalance(account)
        if(result == None):
            # sql 操作失败，这里暂时都不处理
            return None

        if (result == []):
            return None
        else:
            if (result[0][1] >= value):
                _value = result[0][1] - value
                self.sql.updateBalanceWithoutCommit(account, _value)
                operation = DEPOSIT_OPERATION
                otherAccount = 0
                recordIndex = self.sql.getRecordIndex() + 1
                self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex)
                return (_value,value)
            else:
                return None

    # 转账
    def transfer(self,account,toAccount,value):
        if(value==0):
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        result = self.sql.getBalance(account)
        if(result == [] or result == None):
            return None

        blance = self.sql.getBalance(toAccount)
        if(blance == [] or blance == None):
            return None

        if (result[0][1] >= value):
            _value = result[0][1] - value
            _blance= blance[0][1] + value
            self.sql.updateBalanceWithoutCommit(account, _value)
            self.sql.updateBalanceWithoutCommit(toAccount, _blance)
            operation = TRANSER_OPERATION
            otherAccount = toAccount
            recordIndex = self.sql.getRecordIndex() + 1
            self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex)
            return (_value,value)
        else:
            return None


if __name__ == "__main__":
    # # print(SQL_SEARCH_BALANCE_TABLE)
    # # print(SQL_SEARCH_RECORD_TABLE)
    # # print(SQL_CREATE_BALANCE_TABLE)
    # # print(SQL_CREATE_RECORD_TABLE)
    # test = bankSql()
    # test.connect()
    # # test.insertBalance("xd5", 100)
    # test.updateBalance("xd5", 100)
    # print(test.getBalance("xd5"))
    # test.updateBalance("xd5", 200)
    # print(test.getBalance("xd5"))
    # test.updateBalance("xd5", 100)
    # print(test.getBalance("xd5"))

    # print(test.getBalance("xd1"))
    # print(test.getBalance("xd2"))
    # print(test.getBalance("xd4"))
    # print(test.getBalance("xd5"))
    # print(test.getBalance("xd5")[0][1])
    # # test.insertRecord("xd", 1540975565, DEPOSIT_OPERATION     , "" , 100)
    # # test.insertRecord("xd", 1540975566, WITHDRAWAL_OPERATION  , "" , 100)
    # # test.insertRecord("xd", 1540975567, TRANSER_OPERATION     , "xd1" , 100)
    # # test.insertRecord("xd", 1540975568, TRANSFEROUT_OPERATION , "xd2" , 100)
    #
    # # test.insertRecord("xd", 2540975565, DEPOSIT_OPERATION, "", 100, 1)
    # # test.insertRecord("xd", 2540975566, WITHDRAWAL_OPERATION, "", 100, 2)
    # # test.insertRecord("xd", 2540975567, TRANSER_OPERATION, "xd1", 100, 3)
    # # test.insertRecord("xd", 2540975568, TRANSFEROUT_OPERATION, "xd2", 100, 4)
    #
    # print(test.getRecord("xd"))
    # print(test.getRecord("ad"))
    # test.getRecordIndex()
    # # print(test.getBalance("xd1"))
    # # print(test.getBalance("xd2"))
    # # print(test.getBalance("xd4"))
    # # print(test.getBalance("xd5"))
    # test.close()
    #
    # print(operation.deposit)

    bank=Bank()
    bank.run()

    bank.deposit("xd1", 100)
    bank.deposit("xd2", 100)

    bank.transfer("xd1", "xd2", 0)

    # bank.withdrawal("xd1", bank.getBalance("xd1"))
    # bank.withdrawal("xd2", bank.getBalance("xd2"))
    # bank.withdrawal("xd3", bank.getBalance("xd3"))
    # bank.withdrawal("xd4", bank.getBalance("xd4"))
    # bank.withdrawal("xd5", bank.getBalance("xd5"))

    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    #
    # bank.deposit("xd1", 100)
    # bank.deposit("xd2", 100)
    # bank.deposit("xd3", 100)
    # bank.deposit("xd4", 100)
    # bank.deposit("xd5", 100)
    #
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    # bank.transfer("xd1", "xd2", 100)
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    #
    # bank.transfer("xd2", "xd3", 100)
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    #
    # bank.transfer("xd3", "xd4", 100)
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    #
    # bank.transfer("xd4", "xd5", 100)
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    #
    # bank.transfer("xd5", "xd1", 100)
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")


    #
    # bank.withdrawal("xd1", 10)
    # bank.withdrawal("xd2", 20)
    # bank.withdrawal("xd3", 30)
    # bank.withdrawal("xd4", 40)
    # bank.withdrawal("xd5", 50)
    #
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    # bank.withdrawal("xd1", bank.getBalance("xd1"))
    # bank.withdrawal("xd2", bank.getBalance("xd2"))
    # bank.withdrawal("xd3", bank.getBalance("xd3"))
    # bank.withdrawal("xd4", bank.getBalance("xd4"))
    # bank.withdrawal("xd5", bank.getBalance("xd5"))
    #
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    # bank.withdrawal("xd1", bank.getBalance("xd1"))
    # bank.withdrawal("xd2", bank.getBalance("xd2"))
    # bank.withdrawal("xd3", bank.getBalance("xd3"))
    # bank.withdrawal("xd4", bank.getBalance("xd4"))
    # bank.withdrawal("xd5", bank.getBalance("xd5"))
    #
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    # bank.withdrawal("xd1", 100)
    # bank.withdrawal("xd2", 100)
    # bank.withdrawal("xd3", 100)
    # bank.withdrawal("xd4", 100)
    # bank.withdrawal("xd5", 100)
    #
    # print(bank.getBalance("xd1"))
    # print(bank.getBalance("xd2"))
    # print(bank.getBalance("xd3"))
    # print(bank.getBalance("xd4"))
    # print(bank.getBalance("xd5"))
    # print("--------------------------")
    # print(bank.sql.getRecord("xd1"))
    # print(len(bank.sql.getRecord("xd1")))

    # bank = Bank("test.db")
    # bank.run()
    #
    # bank.deposit("xd1", 100)