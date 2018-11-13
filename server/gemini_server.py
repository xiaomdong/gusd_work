from concurrent import futures
import time
import threading
import grpc
import sys

import gemini_pb2
import gemini_pb2_grpc
import gemini_sql
import control


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

sys.path.append("/home/test/PycharmProjects/gusd_work/server")

class gemini_server(gemini_pb2_grpc.geminiServicer):
    def __init__(self):
        super(gemini_server, self).__init__()
        self.gemini_sql=gemini_sql.gemini()
        self.gemini_sql.run()
        control.gusd_init()
        self.threadLock = threading.Lock()

    # 用户登录
    def login(self, request, context):
        self.threadLock.acquire()
        user=self.gemini_sql.sql.getUser(request.account)
        self.threadLock.release()
        if(user == None or user == []):
            return gemini_pb2.balanceReply(message='ERR')

        if(request.password != user[1]):
            return gemini_pb2.balanceReply(message='ERR')

        return gemini_pb2.loginReply(message='OK')

    # 用户注册
    def register(self, request, context):
        self.threadLock.acquire()
        DepositEthaddress=control.create_eth_addr()
        self.gemini_sql.addUser(self,
                                request.account,
                                request.password,
                                request.mail,
                                request.phone,
                                request.withdrawBankAccount,
                                request.withdrawEthaddress,
                                DepositEthaddress)
        self.threadLock.release()
        return gemini_pb2.registerReply(message='OK')


    # 获取用户余额
    # GUSD可以不加入到数据库中,暂时不改写此处代码
    def balance(self, request, context):
        self.threadLock.acquire()
        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance==[] ):
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        user=self.gemini_sql.sql.getUser(request.account)
        if(user == None or user == []):
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        usdValue=user[7]
        DepositEthaddress=user[6]
        gusdValue=control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()

        if (balance[0] != usdValue):
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        if (balance[1] != gusdValue):
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        return gemini_pb2.balanceReply(message='OK',usd=usdValue,gusd=gusdValue)

    # 查询用户信息
    def info(self, request, context):
        self.threadLock.acquire()
        user=self.gemini_sql.sql.getUser(request.account)

        if(user == None or user == []):
            return gemini_pb2.infoReply(message='OK',
                                        account=request.account,
                                        mail='None',
                                        phone='None',
                                        usd=0,
                                        gusd=0,
                                        depositEthaddress='None',
                                        depositBankAccount='None',
                                        withdrawBankAccount='None',
                                        withdrawEthaddress='None')
        DepositEthaddress=user[6]
        gusdValue=control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()

        return gemini_pb2.infoReply(message='OK',
                                    account=user[0],
                                    mail=user[1],
                                    phone=user[2],
                                    usd=user[7],
                                    gusd=gusdValue,
                                    depositEthaddress=user[6],
                                    depositBankAccount=control.REGULATORY_BANK_ACCOUNT,
                                    withdrawBankAccount = user[4],
                                    withdrawEthaddress = user[5])


    # USD兑换GUSD
    # USD减少
    # GUSD增加
    # 如果sweeper账户有足够的GUSD，将GUSD转账给兑换用户
    # 如果sweeper账户没有足够的GUSD，从归集账户转账value到监管账户
    #   向sweeper账户发行value的GUSD，然后将value的GUSD转账到兑换用户
    # 没有添加异常处理
    def exchangeGUSD(self, request, context):
        self.threadLock.acquire()
        # request.account
        # request.usd

        #获取USD余额
        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance==[] ):
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)
        if(request.usd > balance[0] ): #如果余额小于兑换数目
            return gemini_pb2.balanceReply(message='Insufficient balance', usd=0, gusd=0)

        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None or user == []):
            return gemini_pb2.exchangeGUSDReply(message='ERR', usd=0, gusd=0)
        DepositEthaddress = user[6]

        # 获取sweeper地址的GUSD余额
        sweeperGusdValue = control.getGUSDBalance(0xa8512Eab06Ed25F8452Bf7A99E5C65135f822bF3)


        if(sweeperGusdValue < request.usd):
            # sweeper账户没有足够的GUSD
            # 从归集账户向监管账户转账
            # 发行GUSD
            control.gusd_print(request.usd)

        # sweeper账户有足够的GUSD，将GUSD转账给兑换用户
        control.sweeperTransfer(DepositEthaddress,request.usd)
        balance=self.gemini_sql.exchangeGUSD(request.account,request.usd)
        if(balance == None or balance==[] ):
            #失败需要回退，待添加
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        usdValue = balance[0]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()
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
            return gemini_pb2.exchangeGUSDReply(message='ERR', usd=0, gusd=0)

        DepositEthaddress = user[6]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        if(request.gusd > gusdValue ):#如果余额小于兑换数目
            return gemini_pb2.exchangeUSDReply(message='Insufficient balance', usd=100, gusd=100)

        control.transferToSweeper(DepositEthaddress,request.gusd)
        balance=self.gemini_sql.exchangeUSD(request.account,request.gusd)
        if(balance == None or balance==[] ):
            #失败需要回退，待添加
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)

        usdValue = balance[0]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()
        return gemini_pb2.exchangeUSDReply(message='OK',usd=usdValue,gusd=gusdValue)

    #提现USD
    def withdrawalUSD(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.withdrawalUSDReply(message='OK',usd=100,gusd=100)

    # 提现GUSD
    # 从客户账户转账到客户提现GUSD账户
    def withdrawalGUSD(self, request, context):
        self.threadLock.acquire()
        # transfer
        #
        # string
        # account = 1;
        # string
        # withdrawEthaddress = 2;
        # uint32
        # gusd = 3;
        user = self.gemini_sql.sql.getUser(request.account)
        if (user == None or user == []):
            return gemini_pb2.exchangeGUSDReply(message='ERR', usd=0, gusd=0)

        DepositEthaddress = user[6]
        gusdValue = control.getGUSDBalance(DepositEthaddress)
        if(request.gusd > gusdValue ):#如果余额小于兑换数目
            return gemini_pb2.exchangeUSDReply(message='Insufficient balance', usd=0, gusd=0)


        control.transfer(DepositEthaddress,request.withdrawEthaddress,gusdValue)

        balance = self.gemini_sql.getBalance(request.account)
        if(balance == None or balance==[] ):
            return gemini_pb2.balanceReply(message='ERR', usd=0, gusd=0)
        usdValue = balance[0]

        gusdValue = control.getGUSDBalance(DepositEthaddress)
        self.threadLock.release()
        return gemini_pb2.withdrawalGUSDReply(message='OK',usd=100,gusd=gusdValue)


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
    def bankInfo(self,request, context):
        print(request)
        self.threadLock.acquire()
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