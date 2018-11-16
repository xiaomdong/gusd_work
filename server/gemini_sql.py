import log
g_log=log.getLogging(__name__)

import sqlite3
import datetime
from enum import Enum
import control

GEMINI_SQL_DB = "gemini.db"
USER_TABLE = "user"
RECORD_TABLE = "record"  # 收到的银行转账记录设置USD存入记录？，USD兑换GUSD记录，GUSD兑换USD记录,USD提现记录，GUSD提现记录，GUSD存入记录
COMPANY_TABLE = "company"

SQL_SEARCH_USER_TABLE = "select * from sqlite_master where type = 'table' and name = '%s'" % (USER_TABLE)
SQL_SEARCH_RECORD_TABLE = "select * from sqlite_master where type = 'table' and name = '%s'" % (RECORD_TABLE)

SQL_CREATE_USER_TABLE = "create table %s (account text primary key, password text, mail text, phone text, withdrawBankAccount text, withdrawEthaddress text, DepositEthaddress text, USD integer, GUSD integer)" % (
    USER_TABLE)
SQL_CREATE_RECORD_TABLE = "create table %s (account text, time  text, operation integer, otherAccount text, value integer, recordIndex integer primary key, addedinfo text)" % (
    RECORD_TABLE)

SQL_INSERT_USER_TABLE = "insert into %s values (?,?,?,?,?,?,?,?,?)" % (USER_TABLE)
SQL_UPDATE_USER_TABLE = "update %s set password=?,mail=?,phone=?,withdrawBankAccount=?,withdrawEthaddress=?,DepositEthaddress=? where account=?" % (USER_TABLE)
SQL_SELECT_USER_TABLE = "select * from %s where account=?" % (USER_TABLE)
SQL_UPDATE_GUSD_USER_TABLE = "update %s set gusd=? where account=?" % (USER_TABLE)
SQL_UPDATE_USD_USER_TABLE = "update %s set usd=? where account=?" % (USER_TABLE)
SQL_GETBALANCE_USER_TABLE = "select usd,gusd from %s where account=?" % (USER_TABLE)

SQL_UPDATE_USD_GUSD_USER_TABLE = "update %s set usd=? gusd=? where account=?" % (USER_TABLE)

SQL_INSERT_RECORD_TABLE = "insert into %s values (?,?,?,?,?,?,?)" % (RECORD_TABLE)
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
DEPOSIT_REGULATORY_USD_OPERATION = 8       #未使用 监管账户存款
WITHDRAWAL_REGULATORY_USD_OPERATION = 9    #未使用 监管账户提取到归结账户
BURN_GUSD_OPERATION = 10                   #未使用 sweeper账户燃烧gusd
PRINT_GUSD_OPERATION = 11                  #未使用 sweeper账户发行gusd


COMPANY_BANK_COLLECTION_ACCOUNT  = control.COLLECTIVE_BANK_ACCOUNT
COMPANY_BANK_REGULATORY_ACCOUNT = control.REGULATORY_BANK_ACCOUNT
COMPANY_SERVER_SWEEPER_ADDRESS = control.SWEEPER_ETH_ACCOUNT

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
            g_log.info("SQL_CREATE_BALANCE_TABLE ")
        else:
            g_log.info("exist %s table" % (USER_TABLE))

        self.cursor.execute(SQL_SEARCH_RECORD_TABLE)
        result = self.cursor.fetchall();
        if (len(result) == 0):
            self.cursor.execute(SQL_CREATE_RECORD_TABLE)
            self.conn.commit()
            g_log.info("SQL_CREATE_RECORD_TABLE ")
        else:
            g_log.info("exist %s table" % (RECORD_TABLE))

    def runSqlwithCommit(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            return []   #表示执行正常
        except Exception as e:
            self.conn.rollback() # 回滚？
            g_log.error("something err:%s" % (e))
            return None #表示执行异常

    def runSqlWithoutCommit(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.cursor.fetchall();
            return []     #表示执行正常
        except Exception as e:
            self.conn.rollback()  # 回滚？
            g_log.error("something err:%s" % (e))
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
            g_log.error("something err:%s" % (e))
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
            g_log.error("something err:%s" % (e))
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

    def updateBalanceWithoutCommit(self, account,usd,gusd):
        tmp = (account,usd,gusd)
        return self.runSqlWithoutCommit(SQL_UPDATE_USD_GUSD_USER_TABLE, tmp)

    def updateBalance(self, account,usd,gusd):
        tmp = (account,usd,gusd)
        return self.runSql(SQL_UPDATE_USD_GUSD_USER_TABLE, tmp)

    def insertRecord(self, account, time, operation, otherAccount, value, recordIndex, addedinfo):
        tmp = (account, time, operation, otherAccount, value, recordIndex, addedinfo)
        # print(tmp)
        return self.runSqlwithCommit(SQL_INSERT_RECORD_TABLE, tmp)

    def getRecord(self, account):
        tmp = (account,account)
        return self.runSql(SQL_SELECT_RECORD_TABLE, tmp)

    def getRecordIndex(self):
        result = self.runSqlWithoutData(SQL_SELECT_ALL_RECORD_TABLE)
        if(result==None):
            return None
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
    # addedinfo，信息为""
    def addUser(self, account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress, addedinfo=""):
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
            if(recordIndex==None):
                return None
            if (self.sql.insertRecord(account, time, operation, otherAccount, 0, recordIndex , addedinfo) == None):
                # sql 操作失败，这里暂时都不处理
                return None
        else:
            if(self.sql.updateUserWithoutCommit(account, password, mail, phone, withdrawBankAccount, withdrawEthaddress, DepositEthaddress) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            operation=UPDATE_USER_OPERATION
            otherAccount = account + "," + password + "," + mail + "," + phone + "," + withdrawBankAccount + "," + withdrawEthaddress + "," + DepositEthaddress + ","
            recordIndex = self.sql.getRecordIndex() + 1
            if(recordIndex==None):
                return None
            if (self.sql.insertRecord(account, time, operation, otherAccount, 0, recordIndex, addedinfo) == None):
                # sql 操作失败，这里暂时都不处理
                return None
        return "OK"


    # 存款USD,由客户向归集账户转账发起，bank_server发现归集账户余额发生变化事会以RPC方式通知gemini_server，rpc事件分析后，调用此函数
    # addedinfo 记录客户向归集账户转账的交易记录recordIndex
    def depositUSD(self, account, value, addedinfo):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = self.sql.getBalance(account)
        if(result == None):
            # sql 操作失败，这里暂时都不处理
            return None

        if (result == []):
            #没有查询到用户的记录
            # return "NO_USER"
            return None
        else:
            _value = result[0][0] + value #[0][0]是USD [0][1]是GUSD
            if(self.sql.updateUSDWithoutCommit(account, _value) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            operation = DEPOSIT_USD_OPERATION
            otherAccount = COMPANY_BANK_COLLECTION_ACCOUNT  #银行归集账户
            recordIndex = self.sql.getRecordIndex() + 1
            if(recordIndex==None):
                return None
            if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
                # sql 操作失败，这里暂时都不处理
                return None
            return  (_value,value) #返回存款的USD余额，和存款的数目

    # 提现USD,此函数调用后，接着调用归集账户向客户的提现账户转账
    # addedinfo 记录归集账户向客户转账的银行交易记录recordIndex
    def withdrawalUSD(self, account, value, addedinfo):
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
                if (recordIndex == None):
                    return None
                if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                return (_value,value) #返回提现后的USD余额，和提现的数目
            else:
                return None

    # gusd兑换USD
    # 客户的DepositEthaddress向SWEEPER地址转账
    # 表示客户用手中的GUSD兑换成USD
    # addedinfo记录客户的DepositEthaddress向SWEEPER地址转账的交易哈希
    def exchangeUSD(self, account, value, addedinfo):
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
                _value = result[0][0] + value
                if(self.sql.updateUSDWithoutCommit(account, _value) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                operation = EXCHANGE_USD_OPERATION
                otherAccount = COMPANY_SERVER_SWEEPER_ADDRESS #银行归集账户
                recordIndex = self.sql.getRecordIndex() + 1
                if (recordIndex == None):
                    return None
                if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                return (_value,value) #返回兑换后的USD余额，和兑换的数目
            else:
                return None

    # 存款GUSD，由客户触发，web3模块收到转账event后调用此函数
    # addedinfo记录客户的DepositEthaddress接收到GUSD的交易哈希
    # 暂时废弃不用
    def depositGUSD(self, account, value, addedinfo):
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
            if(recordIndex==None):
                return None
            if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
                # sql 操作失败，这里暂时都不处理
                return None

            return (_value, value)  # 返回存款的GUSD余额，和存款的数目


    # 提现GUSD,通过web3模块调用gusd转账，从SWEEPER地址向客户提现的GUSD地址转账
    # addedinfo记录客户的DepositEthaddress地址转出GUSD的交易哈希
    # 暂时废弃不用
    def withdrawalGUSD(self, account, value, addedinfo):
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
                if (recordIndex == None):
                    return None
                if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                return (_value,value)
            else:
                return None


    # usd兑换GUSD,usd账户减少，gusd账户增加，总和不变
    # SWEEPER地址向客户的DepositEthaddress地址转账
    # 表示客户用手中的USD兑换成GUSD
    # addedinfo记录SWEEPER地址向客户的DepositEthaddress地址转账的交易哈希
    def exchangeGUSD(self, account, value, addedinfo):
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
            if (result[0][0] >= value): #[0][0]是USD [0][1]是GUSD
                _value = result[0][0] - value
                if(self.sql.updateUSDWithoutCommit(account, _value) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                operation = EXCHANGE_GUSD_OPERATION
                otherAccount = COMPANY_SERVER_SWEEPER_ADDRESS
                recordIndex = self.sql.getRecordIndex() + 1
                if (recordIndex == None):
                    return None
                if(self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
                    # sql 操作失败，这里暂时都不处理
                    return None
                return (_value,value) #返回兑换后的USD余额，和兑换的数目
            else:
                return None


    # record burn gusd
    # addedinfo将记录发行的交易哈希
    def burnGUSD(self,value,addedinfo):
        if(value==0):
            # 提现0，不用操作
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        account   = COMPANY_SERVER_SWEEPER_ADDRESS
        operation = BURN_GUSD_OPERATION
        otherAccount = "0"
        recordIndex = self.sql.getRecordIndex() + 1
        if (recordIndex == None):
            return None
        if (self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
            # sql 操作失败，这里暂时都不处理
            return None


    # record print gusd
    # addedinfo将记录发行的交易哈希
    def printGUSD(self,value,addedinfo):
        if(value==0):
            # 提现0，不用操作
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        account = "0"
        operation = PRINT_GUSD_OPERATION
        otherAccount = COMPANY_SERVER_SWEEPER_ADDRESS
        recordIndex = self.sql.getRecordIndex() + 1
        if (recordIndex == None):
            return None
        if (self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
            # sql 操作失败，这里暂时都不处理
            return None


    #record deposit USD to regulatory
    #addedinfo将记录银行的recordindex，表示从归集账户向监管账户转账的事件记录
    def depositUSD2Regulatory(self,value,addedinfo):
        if(value==0):
            # 提现0，不用操作
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        account = COMPANY_BANK_COLLECTION_ACCOUNT
        operation = DEPOSIT_REGULATORY_USD_OPERATION
        otherAccount = COMPANY_BANK_REGULATORY_ACCOUNT
        recordIndex = self.sql.getRecordIndex() + 1
        if (recordIndex == None):
            return None
        if (self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
            # sql 操作失败，这里暂时都不处理
            return None


    #record withdrawal USD to Collection
    #addedinfo将记录银行的recordindex，表示从监管账户向归集账户转账的事件记录
    def withdrawalUSD2Collection(self,value,addedinfo):
        if(value==0):
            # 提现0，不用操作
            return None

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        account = COMPANY_BANK_REGULATORY_ACCOUNT
        operation = WITHDRAWAL_REGULATORY_USD_OPERATION
        otherAccount = COMPANY_BANK_COLLECTION_ACCOUNT
        recordIndex = self.sql.getRecordIndex() + 1
        if (recordIndex == None):
            return None
        if (self.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo) == None):
            # sql 操作失败，这里暂时都不处理
            return None

