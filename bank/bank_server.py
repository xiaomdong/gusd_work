import log
g_log=log.getLogging(__name__)

from concurrent import futures
import time
import threading
import grpc

import bank_pb2
import bank_pb2_grpc
import bank_sql

# from bank import bank_pb2
# from bank import bank_pb2_grpc
# from bank import bank_sql


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class bank_server(bank_pb2_grpc.bankServicer):
    def __init__(self):
        super(bank_server, self).__init__()
        self.bankSql=bank_sql.bank()
        self.bankSql.run()
        self.threadLock = threading.Lock()

    def deposit(self, request, context):
        # g_log.info(request)
        g_log.info("deposit: "+ request.account + " " + str(request.value))
        self.threadLock.acquire()
        recordIndex_=self.bankSql.deposit(request.account,request.value)
        if(recordIndex_==None):
            self.threadLock.release()
            return bank_pb2.depositReply(message='ERR', balance=0, recordIndex=0)
        result=self.bankSql.getBalance(request.account)
        self.threadLock.release()
        if(result==None):
            return bank_pb2.depositReply(message='ERR', balance=0, recordIndex=recordIndex_)
        return bank_pb2.depositReply(message='OK',balance=result,recordIndex=recordIndex_)

    def withdrawal(self, request, context):
        g_log.info("withdrawal: " + request.account + " " + str(request.value))
        self.threadLock.acquire()
        result=self.bankSql.withdrawal(request.account,request.value)
        if(result==None):
            self.threadLock.release()
            return bank_pb2.withdrawalReply(message='ERR', balance=0, recordIndex=0)
        recordIndex_=result[0]
        result = self.bankSql.getBalance(request.account)
        self.threadLock.release()
        if (result == None):
            return bank_pb2.withdrawalReply(message='ERR', balance=0, recordIndex=recordIndex_)
        return bank_pb2.withdrawalReply(message='OK',balance=result,recordIndex=recordIndex_)

    def balance(self, request, context):
        g_log.info("balance: " + request.account)
        self.threadLock.acquire()
        result = self.bankSql.getBalance(request.account)
        if(request==None):
            return bank_pb2.balanceReply(message='ERR', balance=0)
        self.threadLock.release()
        return bank_pb2.balanceReply(message='OK',balance=result)

    def transfer(self, request, context):
        g_log.info("transfer:" + request.fromAccount + " to " + request.toAccount + str(request.value))
        self.threadLock.acquire()
        result = self.bankSql.transfer(request.fromAccount,request.toAccount,request.value)
        if(result ==None):
            self.threadLock.release()
            return bank_pb2.transferReply(message='ERR', balance=0, recordIndex=0)
        recordIndex_ = result[0]
        result = self.bankSql.getBalance(request.fromAccount)
        self.threadLock.release()
        if(result==None):
            return bank_pb2.transferReply(message='ERR', balance=0, recordIndex=recordIndex_)
        return bank_pb2.transferReply(message='OK',balance=result,recordIndex=recordIndex_)

    def getRecord(self, request, context):
        # print("getRecord")
        # print(request)
        g_log.info("getRecord: " + request.account)
        records = self.bankSql.sql.getRecord(request.account)
        # print(records)
        feature_list = []
        for record in records:
            feature = bank_pb2.getRecordReply(account=record[0], time=record[1], operation=record[2], otherAccount=record[3], value=record[4])
            feature_list.append(feature)
        # print(feature_list)
        for i in feature_list:
            yield i

        # feature_list = []
        # feature = self.bank_pb2.getRecordReply(account='yl002', flag=True, value=100, time=123)
        # feature_list.append(feature)
        # feature = bank_pb2.getRecordReply(account='yl003', flag=True, value=200, time=456)
        # feature_list.append(feature)
        # feature = bank_pb2.getRecordReply(account='yl004', flag=True, value=300, time=789)
        # feature_list.append(feature)
        # for i in feature_list:
        #     yield i

def run():
    g_log.info("server start")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_bankServicer_to_server(bank_server(), server)
    server.add_insecure_port('[::]:50052')
    g_log.info("server run in [::]:50052")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()