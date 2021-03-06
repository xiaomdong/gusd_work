# python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./gemini.proto
import log
g_log=log.getLogging(__name__)

import datetime
from concurrent import futures
import time
import threading
import grpc

# import sys
# sys.path.append("/home/test/PycharmProjects/gusd_work/server")

import gemini_pb2
import gemini_pb2_grpc
import gemini_sql
import control
from bank import bank_sql

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class gemini_server(gemini_pb2_grpc.geminiServicer):
    def __init__(self):
        super(gemini_server, self).__init__()
        self.gemini_sql=gemini_sql.gemini()
        self.gemini_sql.run()
        control.gusd_init()
        control.setEventRecordFun(self.gemini_sql.burnGUSD,
                                  self.gemini_sql.printGUSD,
                                  self.gemini_sql.depositUSD2Regulatory,
                                  self.gemini_sql.withdrawalUSD2Collection,
                                  self.gemini_sql.depositGUSDRecord)

        control.event_thread_run()
        self.threadLock = threading.Lock()

    # 用户登录
    def login(self, request, context):
        self.threadLock.acquire()
        user=self.gemini_sql.sql.getUser(request.account)
        self.threadLock.release()
        if(user == None or user == []):
            return gemini_pb2.loginReply(message='SQL GET USER ERR')

        if(request.password != user[1]):
            return gemini_pb2.loginReply(message='PASSWORD ERR')

        return gemini_pb2.loginReply(message='OK')

    # 用户注册
    def register(self, request, context):
        g_log.info("register user be called")
        self.threadLock.acquire()
        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None):
            return gemini_pb2.registerReply(message='SQL RUN ERR')

        DepositEthaddress=[]
        if(user == []):
            DepositEthaddress=control.create_eth_addr()
            if(DepositEthaddress==None):
                self.threadLock.release()
                return gemini_pb2.registerReply(message='WEB3 CREATE ETH ADDRESS ERR')
        else:
            DepositEthaddress=user[0][6]

        result=self.gemini_sql.addUser(
                                request.account,
                                request.password,
                                request.mail,
                                request.phone,
                                request.withdrawBankAccount,
                                request.withdrawEthaddress,
                                DepositEthaddress)
        self.threadLock.release()
        if(result==None):
            return gemini_pb2.registerReply(message='SQL ADD USER ERR')
        return gemini_pb2.registerReply(message='OK')

    # 获取用户余额
    # GUSD可以不加入到数据库中,暂时不改写此处代码
    def balance(self, request, context):
        self.threadLock.acquire()
        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance==[] ):
            self.threadLock.release()
            return gemini_pb2.balanceReply(message='SQL GET BALANCE ERR', usd=0, gusd=0)

        user=self.gemini_sql.sql.getUser(request.account)
        if(user == None or user == []):
            self.threadLock.release()
            return gemini_pb2.balanceReply(message='SQL GET USER ERR', usd=0, gusd=0)

        usdValue=user[0][7]
        DepositEthaddress=user[0][6]
        gusdValue=control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()

        if(gusdValue == None):
            return gemini_pb2.balanceReply(message='WEB3 GET USER GUSD BALANCE ERR', usd=0, gusd=0)

        if (balance[0][0] != usdValue):
            return gemini_pb2.balanceReply(message='USD BALANCE ERR', usd=0, gusd=0)

        # balance[1]暂时不用
        # if (balance[1] != gusdValue):
        #     return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        return gemini_pb2.balanceReply(message='OK',usd=usdValue,gusd=gusdValue)

    # 查询用户信息
    def info(self, request, context):
        self.threadLock.acquire()
        user=self.gemini_sql.sql.getUser(request.account)

        if(user == None or user == []):
            self.threadLock.release()
            return gemini_pb2.infoReply(message='SQL GET USER ERR',
                                        account=request.account,
                                        mail='None',
                                        phone='None',
                                        usd=0,
                                        gusd=0,
                                        depositEthaddress='None',
                                        depositBankAccount='None',
                                        withdrawBankAccount='None',
                                        withdrawEthaddress='None')
        DepositEthaddress=user[0][6]
        gusdValue=control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()

        if(gusdValue==None):
            return gemini_pb2.infoReply(message='WEB3 GET USER GUSD BALANCE ERR',
                                        account=user[0][0],
                                        mail=user[0][1],
                                        phone=user[0][2],
                                        usd=user[0][7],
                                        gusd=0,
                                        depositEthaddress=user[0][6],
                                        depositBankAccount=control.REGULATORY_BANK_ACCOUNT,
                                        withdrawBankAccount=user[0][4],
                                        withdrawEthaddress=user[0][5])

        return gemini_pb2.infoReply(message='OK',
                                    account=user[0][0],
                                    mail=user[0][1],
                                    phone=user[0][2],
                                    usd=user[0][7],
                                    gusd=gusdValue,
                                    depositEthaddress=user[0][6],
                                    depositBankAccount=control.REGULATORY_BANK_ACCOUNT,
                                    withdrawBankAccount = user[0][4],
                                    withdrawEthaddress = user[0][5])

    # USD兑换GUSD
    # USD减少
    # GUSD增加
    # 如果sweeper账户有足够的GUSD，将GUSD转账给兑换用户
    # 如果sweeper账户没有足够的GUSD，从归集账户转账value到监管账户
    #   向sweeper账户发行value的GUSD，然后将value的GUSD转账到兑换用户
    # 没有添加异常处理
    def exchangeGUSD(self, request, context):
        g_log.info(request)
        self.threadLock.acquire()
        # request.account
        # request.usd

        #获取USD余额
        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance==[] ):
            self.threadLock.release()
            return gemini_pb2.exchangeGUSDReply(message='WEB3 GET USER GUSD BALANCE ERR', usd=0, gusd=0)

        if(request.usd > balance[0][0] ): #如果余额小于兑换数目
            self.threadLock.release()
            return gemini_pb2.exchangeGUSDReply(message='INSUFFICIENT USD BALANCE', usd=0, gusd=0)

        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None or user == []):
            self.threadLock.release()
            return gemini_pb2.exchangeGUSDReply(message='SQL GET USER ERR', usd=0, gusd=0)
        DepositEthaddress = user[0][6]

        # 获取sweeper地址的GUSD余额
        sweeperGusdValue = control.getGUSDBalance(control.SWEEPER_ETH_ACCOUNT)
        if(sweeperGusdValue==None):
            self.threadLock.release()
            return gemini_pb2.exchangeGUSDReply(message='WEB3 GET SWEEPER GUSD BALANCE ERR', usd=0, gusd=0)

        self.threadLock.release()
        if(sweeperGusdValue < request.usd):
            # sweeper账户没有足够的GUSD
            # 从归集账户向监管账户转账
            # 发行GUSD
            if(control.gusd_print(request.usd)==None):
                return gemini_pb2.exchangeGUSDReply(message='WEB3 PRINT GUSD ERR', usd=0, gusd=0)

        self.threadLock.acquire()
        # sweeper账户有足够的GUSD，将GUSD转账给兑换用户
        txhash=control.sweeperTransfer(DepositEthaddress,request.usd)
        if(txhash==None):
            self.threadLock.release()
            return gemini_pb2.exchangeGUSDReply(message='WEB3 SWEEPER TRANSFER GUSD TO USER ERR', usd=0, gusd=0)

        balance=self.gemini_sql.exchangeGUSD(request.account,request.usd, txhash)

        if(balance == None or balance==[] ):
            #失败需要回退，待添加
            self.threadLock.release()
            return gemini_pb2.exchangeGUSDReply(message='SQL EXCHANGE GUSD ERR', usd=0, gusd=0)

        usdValue = balance[0][0]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()
        if (gusdValue == None):
            return gemini_pb2.exchangeGUSDReply(message='WEB3 GET USER GUSD BALANCE ERR', usd=0, gusd=0)
        return gemini_pb2.exchangeGUSDReply(message='OK',usd=usdValue,gusd=gusdValue)

    # GUSD兑换USD
    # GUSD减少
    # USD增加
    # 向Sweeper账戶转账 value GUSD
    # 设置客戶 USD 余额增加 value 美金
    # 没有添加异常处理
    def exchangeUSD(self, request, context):
        self.threadLock.acquire()
        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None or user == []):
            self.threadLock.release()
            return gemini_pb2.exchangeUSDReply(message='SQL GET USER ERR', usd=0, gusd=0)

        DepositEthaddress = user[0][6]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        if(request.gusd > gusdValue ):#如果余额小于兑换数目
            self.threadLock.release()
            return gemini_pb2.exchangeUSDReply(message='INSUFFICIENT GUSD BALANCE', usd=0, gusd=gusdValue)

        txhash = control.transferToSweeper(DepositEthaddress,request.gusd)
        if(txhash==None):
            self.threadLock.release()
            return gemini_pb2.exchangeUSDReply(message='WEB3 USER TRANSFER GUSD TO SWEEPER ERR', usd=0, gusd=0)

        balance=self.gemini_sql.exchangeUSD(request.account, request.gusd, txhash)
        if(balance == None or balance==[] ):
            #失败需要回退，待添加
            self.threadLock.release()
            return gemini_pb2.exchangeUSDReply(message='SQL EXCHANGE USD ERR', usd=0, gusd=0)

        usdValue = balance[0][0]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()

        if(gusdValue == None):
            self.threadLock.release()
            return gemini_pb2.exchangeUSDReply(message='WEB3 GET USER GUSD BALANCE ERR', usd=0, gusd=0)

        return gemini_pb2.exchangeUSDReply(message='OK',usd=usdValue,gusd=gusdValue)

    # 提现USD
    # 如果 value 小于 Gemini 的银行归集帐号余额,从银行归集帐号向客戶转账 value 美元
    # 如果 value 大于 Gemini 的银行归集帐号余额:
    # 1.Gemini 从银行监管账戶向银行归集帐号转账 value 美元,
    # 2.Sweeper 地址向 0 地址转账 value GUSD, burn 操作，设置 GUSD totalsupply 减少 value
    # 3.从银行归集帐号向客戶转账 value 美元
    def withdrawalUSD(self, request, context):
        # self.threadLock.acquire()

        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None or user == []):
            # self.threadLock.release()
            return gemini_pb2.withdrawalUSDReply(message='SQL GET USER ERR', usd=0, gusd=0)
        DepositEthaddress = user[0][6]

        #获取USD余额
        balance = self.gemini_sql.getBalance(request.account)
        # self.threadLock.release()

        if(balance == None or balance==[] ):
            return gemini_pb2.withdrawalUSDReply(message='SQL GET BALANCE ERR', usd=0, gusd=0)


        if(request.usd > balance[0][0]):
            return gemini_pb2.withdrawalUSDReply(message='INSUFFICIENT USD BALANCE', usd=balance[0], gusd=0)


        geminiCollectiveBalance = control.bankBlance(control.COLLECTIVE_BANK_ACCOUNT)

        if(geminiCollectiveBalance == None ):
            return gemini_pb2.withdrawalUSDReply(message='SQL GET COLLECTIVE BALANCE ERR', usd=0, gusd=0)


        if(request.usd > geminiCollectiveBalance):
            if(control.bankTransfer(control.REGULATORY_BANK_ACCOUNT,control.COLLECTIVE_BANK_ACCOUNT,request.usd)==None):
                return gemini_pb2.withdrawalUSDReply(message='SQL TRANSFER REGULATORY TO COLLECTIVE ERR', usd=0, gusd=0)

            # self.threadLock.acquire() #锁有冲突，先不锁
            if(control.gusd_burn(request.usd)==None):
                # self.threadLock.release()
                return gemini_pb2.withdrawalUSDReply(message='WEB3 BURN GUSD ERR', usd=0, gusd=0)
            # self.threadLock.release()

        reponse = control.bankTransfer(control.COLLECTIVE_BANK_ACCOUNT, request.withdrawBankAccount, request.usd)
        if(reponse == None):
            return gemini_pb2.withdrawalUSDReply(message='SQL TRANSFER COLLECTIVE TO USER ERR', usd=0, gusd=0)

        print("11111111111111111111")
        self.threadLock.acquire()
        result=self.gemini_sql.withdrawalUSD(request.account,request.usd,str(reponse.recordIndex))
        if(result==None):
            self.threadLock.release()
            return gemini_pb2.withdrawalUSDReply(message='SQL WITHDRAWAL USD ERR', usd=0, gusd=0)
        self.threadLock.release()

        print("22222222222222222222")
        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance == [] ):
            return gemini_pb2.withdrawalUSDReply(message='SQL GET BALANCE ERR', usd=0, gusd=0)

        usdValue = balance[0][0]
        gusdValue = control.getGUSDBalance(DepositEthaddress)

        if (gusdValue == None):
            return gemini_pb2.withdrawalUSDReply(message='WEB3 GET USER GUSD BALANCE ERR', usd=0, gusd=0)

        return gemini_pb2.withdrawalUSDReply(message='OK',usd=usdValue, gusd=gusdValue)

    # 提现GUSD
    # 从客户账户转账到客户提现GUSD账户
    def withdrawalGUSD(self, request, context):
        self.threadLock.acquire()
        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None or user == []):
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='SQL GET USER ERR', usd=0, gusd=0)

        DepositEthaddress = user[0][6]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        if(gusdValue == None):
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='WEB3 GET USER GUSD BALANCE ERR', usd=0, gusd=0)

        if(request.gusd > gusdValue ):#如果余额小于兑换数目
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='INSUFFICIENT GUSD BALANCE', usd=0, gusd=0)

        txhash = control.transfer(DepositEthaddress, request.withdrawEthaddress, request.gusd)
        if(txhash == None):
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='WEB3 TRANSFER GUSD ERR', usd=0, gusd=0)

        # if(self.gemini_sql.withdrawalGUSD(request.account, request.gusd, txhash)==None):
        #     self.threadLock.release()
        #     return gemini_pb2.withdrawalGUSDReply(message='SQL WITHDRAWAL GUSD ERR', usd=0, gusd=0)

        if(self.gemini_sql.withdrawalGUSDRecord(request.account, request.gusd, txhash)==None):
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='SQL WITHDRAWAL GUSD ERR', usd=0, gusd=0)

        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance == [] ):
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='SQL GET BALANCE ERR', usd=0, gusd=0)

        usdValue = balance[0][0]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()

        if(gusdValue == None):
            return gemini_pb2.withdrawalGUSDReply(message='SQL GET GUSD BALANCE ERR', usd=0, gusd=0)
        return gemini_pb2.withdrawalGUSDReply(message='OK', usd=usdValue, gusd=gusdValue)


    def record(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()

        feature_list = []

        feature = gemini_pb2.recordReply(message='OK', account='xd',time='123123',operation=1,otherAccount='xd2',value=3)
        feature_list.append(feature)
        feature = gemini_pb2.recordReply(message='OK', account='xd2',time='123123',operation=1,otherAccount='xd1',value=3)
        feature_list.append(feature)
        for i in feature_list:
            yield i

    # 银行向gemini传递归集账户变动的事件
    # 银行向gemini传递监管账户变动的事件
    # 这里仅仅处理用户存款通知
    def bankInfo(self, request, context):


        if(request.account == control.REGULATORY_BANK_ACCOUNT or request.account == control.COLLECTIVE_BANK_ACCOUNT):
            return gemini_pb2.bankInfoReply(message='OK')

        self.threadLock.acquire()
        user = self.gemini_sql.sql.getUserByBankAccount(request.account)
        if (user == None or user == []):
            self.threadLock.release()
            return gemini_pb2.withdrawalGUSDReply(message='SQL GET USER ERR')

        account=user[0][0]

        if(request.otherAccount == control.COLLECTIVE_BANK_ACCOUNT and request.operation == bank_sql.TRANSER_OPERATION):
            balance = self.gemini_sql.getBalance(account)
            if (balance == None or balance == []):
                self.threadLock.release()
                return gemini_pb2.bankInfoReply(message='SQL GET BALANCE ERR')

            usdValue = balance[0][0] + request.value
            result=self.gemini_sql.depositUSD(account,request.value,str(request.recordIndex))
            if(result == None):
                self.threadLock.release()
                return gemini_pb2.bankInfoReply(message='SQL DEPOSIT USD ERR')

            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            operation = gemini_sql.DEPOSIT_USD_OPERATION
            otherAccount = control.COLLECTIVE_BANK_ACCOUNT
            value = usdValue
            recordIndex = self.gemini_sql.sql.getRecordIndex() + 1
            if(recordIndex==None):
                self.threadLock.release()
                return gemini_pb2.bankInfoReply(message='SQL GET RECORDINDEX ERR')

            addedinfo = request.recordIndex #附加信息用于记录银行交易的记录号
            if(self.gemini_sql.sql.insertRecord(account, time, operation, otherAccount, value, recordIndex, addedinfo)==None):
                self.threadLock.release()
                return gemini_pb2.bankInfoReply(message='SQL INSERT RECORD ERR')

        self.threadLock.release()
        return gemini_pb2.bankInfoReply(message='OK')

def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gemini_pb2_grpc.add_geminiServicer_to_server(gemini_server(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run()