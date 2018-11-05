import sqlite3
import datetime
from enum import Enum

GEMINI_SQL_DB = "gemini.db"
USER_TABLE = "user"
RECORD_TABLE = "record"  # 收到的银行转账记录设置USD存入记录？，USD兑换GUSD记录，GUSD兑换USD记录,USD提现记录，GUSD提现记录，GUSD存入记录
COMPANY_TABLE = "company"

SQL_SEARCH_USER_TABLE = "select * from sqlite_master where type = 'table' and name = '%s'" % (USER_TABLE)
SQL_SEARCH_RECORD_TABLE = "select * from sqlite_master where type = 'table' and name = '%s'" % (RECORD_TABLE)

SQL_CREATE_USER_TABLE = "create table %s (account text primary key, password text, mail text, phone text, withdrawBankAccount text, withdrawEthaddress text, DepositEthaddress text, USD integer, GUSD integer)" % (
    USER_TABLE)
SQL_CREATE_RECORD_TABLE = "create table %s (account text, time  text, operation integer, otherAccount text, value integer,recordIndex integer primary key)" % (
    RECORD_TABLE)

SQL_INSERT_USER_TABLE = "insert into %s values (?,?,?,?,?,?,?,?,?)" % (USER_TABLE)
SQL_UPDATE_USER_TABLE = "update %s set password=?,mail=?,phone=?,withdrawBankAccount=?,withdrawEthaddress=?,DepositEthaddress=? where account=?" % (USER_TABLE)
SQL_SELECT_USER_TABLE = "select * from %s where account=?" % (USER_TABLE)
SQL_UPDATE_GUSD_USER_TABLE = "update %s set gusd=? where account=?" % (USER_TABLE)
SQL_UPDATE_USD_USER_TABLE = "update %s set usd=? where account=?" % (USER_TABLE)
SQL_GETBALANCE_USER_TABLE = "select usd,gusd from %s where account=?" % (USER_TABLE)

SQL_INSERT_RECORD_TABLE = "insert into %s values (?,?,?,?,?,?)" % (RECORD_TABLE)
SQL_SELECT_RECORD_TABLE = "select * from %s where account=? or otherAccount=?" % (RECORD_TABLE)
SQL_SELECT_ALL_RECORD_TABLE = "select * from %s " % (RECORD_TABLE)

CREATE_USER_OPERATION = 0
UPDATE_USER_OPERATION = 1
DEPOSIT_USD_OPERATION = 2
WITHDRAWAL_USD_OPERATION = 3
DEPOSIT_GUSD_OPERATION = 4
WITHDRAWAL_GUSD_OPERATION = 5
EXCHANGE_USD_OPERATION = 6
EXCHANGE_GUSD_OPERATION = 7
DEPOSIT_SUPERVISION_USD_OPERATION = 8
WITHDRAWAL_SUPERVISION_USD_OPERATION = 9
BURN_GUSD_OPERATION = 10
PRINT_GUSD_OPERATION = 11

COMPANY_BANK_COLLECTION_ACCOUNT = "GEMINI_COLLECTION_ACCOUNT"
COMPANY_BANK_SUPERVISION_ACCOUNT = "GEMINI_SUPERVISION_ACCOUNT"
COMPANY_SERVER_SWEEPER_ADDRESS = "0X12345678"
COMPANY_SERVER_SWEEPER_PASSWORD = "12345678"


class geminiSql():
    def __init__(self, db_path=GEMINI_SQL_DB):
        self.path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.path,check_same_thread=False)
        # self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

        self.cursor.execute(SQL_SEARCH_USER_TABLE)
        result = self.cursor.fetchall();
        if (len(result) == 0):
            self.cursor.execute(SQL_CREATE_USER_TABLE)
            self.conn.commit()
            print("SQL_CREATE_BALANCE_TABLE ")
        else:
            print("exist %s table" % (USER_TABLE))

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
            self.cursor.fetchall();
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

    def getUser(self, account):
        tmp = (account,)
        return self.runSql(SQL_SELECT_USER_TABLE, tmp)

    def insertUserWithoutCommit(self, account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress, USD=0, GUSD=0):
        tmp = (account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress, USD, GUSD)
        return self.runSqlWithoutCommit(SQL_INSERT_USER_TABLE, tmp)

    def insertUser(self, account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress, USD=0, GUSD=0):
        tmp = (account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress, USD, GUSD)
        return self.runSqlwithCommit(SQL_INSERT_USER_TABLE, tmp)

    def updateUserWithoutCommit(self, account, password,mail,phone,withdrawBankAccount,withdrawEthaddress,DepositEthaddress ):
        tmp = (password,mail,phone,withdrawBankAccount,withdrawEthaddress,DepositEthaddress,account)
        return self.runSqlWithoutCommit(SQL_UPDATE_USER_TABLE, tmp)

    def updateUser(self, account, password,mail,phone,withdrawBankAccount,withdrawEthaddress,DepositEthaddress ):
        tmp = (password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress,account)
        return self.runSqlwithCommit(SQL_UPDATE_USER_TABLE, tmp)

    def updateGUSDWithoutCommit(self, account, value):
        tmp = (value,account)
        return self.runSqlWithoutCommit(SQL_UPDATE_GUSD_USER_TABLE, tmp)

    def updateGUSD(self, account, value):
        tmp = (value,account)
        return self.runSqlwithCommit(SQL_UPDATE_GUSD_USER_TABLE, tmp)

    def updateUSDWithoutCommit(self, account, value):
        tmp = (value,account)
        return self.runSqlWithoutCommit(SQL_UPDATE_USD_USER_TABLE, tmp)

    def updateUSD(self, account, value):
        tmp = (value,account)
        return self.runSqlwithCommit(SQL_UPDATE_USD_USER_TABLE, tmp)

    def getBalance(self, account):
        tmp = (account,)
        return self.runSql(SQL_GETBALANCE_USER_TABLE, tmp)

    def insertRecord(self, account, time, operation, otherAccount, value, recordIndex):
        tmp = (account, time, operation, otherAccount, value, recordIndex)
        # print(tmp)
        return self.runSqlwithCommit(SQL_INSERT_RECORD_TABLE, tmp)

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
class gemini():
    def __init__(self, db_path=GEMINI_SQL_DB):
        self.sql = geminiSql(db_path)

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
            return [0,0]
        else:
            return result

    # 创建用户和更新用户
    def addUser(self, account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = self.sql.getUser(account)
        if(result == None):
            # sql执行失败
            return None

        if(result == []):
            if(self.sql.insertUserWithoutCommit(account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress,0,0) == None):
                #sql 操作失败，这里暂时都不处理
                return None
            operation=CREATE_USER_OPERATION
            otherAccount = account + "," + password + "," + mail + "," + phone + "," + withdrawBankAccount + "," + withdrawEthaddress + "," + DepositEthaddress + ","
            recordIndex = self.sql.getRecordIndex() + 1
            if (self.sql.insertRecord(account, time, operation, otherAccount, 0, recordIndex) == None):
                # sql 操作失败，这里暂时都不处理
                return None
        else:
            if(self.sql.updateUserWithoutCommit(account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            operation=UPDATE_USER_OPERATION
            otherAccount = account + "," + password + "," + mail + "," + phone + "," + withdrawBankAccount + "," + withdrawEthaddress + "," + DepositEthaddress + ","
            recordIndex = self.sql.getRecordIndex() + 1
            if (self.sql.insertRecord(account, time, operation, otherAccount, 0, recordIndex) == None):
                # sql 操作失败，这里暂时都不处理
                return None
        return "OK"


    # 存款USD,由客户向归集账户转账发起，bank_server发现归集账户余额发生变化事会以RPC方式通知gemini_server，rpc事件分析后，调用此函数
    def depositUSD(self, account, value):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = self.sql.getBalance(account)
        if(result == None):
            # sql 操作失败，这里暂时都不处理
            return None

        if (result == []):
            #没有查询到用户的记录
            return "NO_USER"
        else:
            _value = result[0][0] + value #[0][0]是USD [0][1]是GUSD
            if(self.sql.updateUSDWithoutCommit(account, _value) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            operation = DEPOSIT_USD_OPERATION
            otherAccount = COMPANY_BANK_COLLECTION_ACCOUNT  #银行归集账户
            recordIndex = self.sql.getRecordIndex() + 1
            if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            return  (_value,value) #返回存款的USD余额，和存款的数目

    # 提现USD,此函数调用后，接着调用归集账户向客户的提现账户转账
    def withdrawalUSD(self, account, value):
        if(value==0):
            # 提现0，不用操作
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        result = self.sql.getBalance(account)

        if (result == []):
            # 没有查询到用户的记录
            return None
        else:
            if (result[0][0] >= value): #[0][0]是USD [0][1]是GUSD
                _value = result[0][0] - value
                if(self.sql.updateUSDWithoutCommit(account, _value) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                operation = WITHDRAWAL_USD_OPERATION
                otherAccount = COMPANY_BANK_COLLECTION_ACCOUNT #银行归集账户
                recordIndex = self.sql.getRecordIndex() + 1
                if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                return (_value,value) #返回提现后的USD余额，和提现的数目
            else:
                return None


    # 存款GUSD，由客户触发，web3模块收到转账event后调用此函数
    def depositGUSD(self, account, value):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        result = self.sql.getBalance(account)
        if(result == None):
            # sql执行失败
            return None

        if (result == []):
            # 查询不到用户数据
            return None
        else:
            _value = result[0][1] + value #[0][0]是USD [0][1]是GUSD
            if( self.sql.updateGUSDWithoutCommit(account, _value) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            operation = DEPOSIT_GUSD_OPERATION
            otherAccount = COMPANY_SERVER_SWEEPER_ADDRESS #SWEEPER地址
            recordIndex = self.sql.getRecordIndex() + 1
            if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex) == None):
                # sql 操作失败，这里暂时都不处理
                return None

            return (_value, value)  # 返回存款的GUSD余额，和存款的数目


    # 提现GUSD,通过web3模块调用gusd转账，从SWEEPER地址向客户提现的GUSD地址转账
    def withdrawalGUSD(self, account, value):
        if(value==0):
            # 提现0，不用操作
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        result = self.sql.getBalance(account)
        if(result == None):
            # sql执行失败
            return None


        if (result == []):
            # 查询不到用户数据
            return None
        else:
            if (result[0][1] >= value): #[0][0]是USD [0][1]是GUSD
                _value = result[0][1] - value
                if(self.sql.updateGUSDWithoutCommit(account, _value) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                operation = WITHDRAWAL_GUSD_OPERATION
                otherAccount = COMPANY_SERVER_SWEEPER_ADDRESS
                recordIndex = self.sql.getRecordIndex() + 1
                if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                return (_value,value)
            else:
                return None
