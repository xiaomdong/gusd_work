from concurrent import futures
import time
import threading
import grpc

import gemini_pb2
import gemini_pb2_grpc
import gemini_sql

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class gemini_server(gemini_pb2_grpc.geminiServicer):
    def __init__(self):
        super(gemini_server, self).__init__()
        # self.bankSql=bank_sql.Bank()
        # self.bankSql.run()
        self.threadLock = threading.Lock()

    def login(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.loginReply(message='OK')

    def register(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.registerReply(message='OK')

    def balance(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.balanceReply(message='OK',usd=100,gusd=100)

    def info(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.infoReply(message='OK',account='xd',mail='xd@gmail.com',phone='18033441090',usd=100,gusd=100,depositEthaddress='eht12334',depositBankAccount='xd001')

    def exchangeGUSD(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.exchangeGUSDReply(message='OK',usd=100,gusd=100)

    def exchangeUSD(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.exchangeUSDReply(message='OK',usd=100,gusd=100)

    def withdrawalUSD(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.withdrawalUSDReply(message='OK',usd=100,gusd=100)

    def withdrawalGUSD(self, request, context):
        self.threadLock.acquire()
        self.threadLock.release()
        return gemini_pb2.withdrawalGUSDReply(message='OK',usd=100,gusd=100)

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