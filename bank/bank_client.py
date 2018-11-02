from __future__ import print_function
import threading
import grpc

import bank_pb2
import bank_pb2_grpc




def run1000_1():
    with grpc.insecure_channel('172.16.1.176:50052') as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        for i in range(1000):
            response = stub.deposit(bank_pb2.depositRequest(account='yl001',value=2))
            if (i % 100 ==0):
                print("run...run1000_1")
        response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
        print("balanceRequest    : account='yl001'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")

def run1000_2():
    with grpc.insecure_channel('172.16.1.176:50052') as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        for i in range(1000):
            response = stub.deposit(bank_pb2.withdrawalRequest(account='yl001',value=1))
            if (i % 100 ==0):
                print("run...run1000_2")

        response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
        print("balanceRequest    : account='yl001'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")

def run1000_3():
    with grpc.insecure_channel('172.16.1.176:50052') as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        for i in range(1000):
            response = stub.deposit(bank_pb2.depositRequest(account='yl002',value=1))
            if (i % 100 ==0):
                print("run...run1000_3")

        response = stub.balance(bank_pb2.balanceRequest(account='yl002'))
        print("balanceRequest    : account='yl002'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")



def run1000_4():
    with grpc.insecure_channel('172.16.1.176:50052') as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        for i in range(1000):
            # response = stub.deposit(bank_pb2.depositRequest(account='yl002',value=1))
            response = stub.transfer(bank_pb2.transferRequest(fromAccount='yl001', toAccount='yl002', value=1))
            if (i % 100 ==0):
                print("run...run1000_4")

        response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
        print("balanceRequest    : account='yl001'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")
        response = stub.balance(bank_pb2.balanceRequest(account='yl002'))
        print("balanceRequest    : account='yl002'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")

def getRecord():
    with grpc.insecure_channel('172.16.1.176:50052') as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
        # print(response)
        responses = stub.getRecord(bank_pb2.getRecordRequest(account='yl001'))
        for response in responses:
            print(response)

        # responses = stub.getRecord(bank_pb2.getRecordRequest(account='yl001'))
        # responses = stub.getRecord(bank_pb2.getRecordRequest(account='yl001'))
        # print("getRecordRequest  : account='yl001'")
        # for response in responses:
        #     print("received          : " + response.account + ", " +str(response.value)+ ", " +str(response.time));
        # print("-------------------------------------------")

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('172.16.1.176:50052') as channel:
        stub = bank_pb2_grpc.bankStub(channel)

        response = stub.deposit(bank_pb2.depositRequest(account='yl001',value=100))
        print("depositRequest    : account='yl001',value=100")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")

        response = stub.withdrawal(bank_pb2.withdrawalRequest(account='yl001',value=100))
        print("withdrawalRequest : account='yl001',value=100")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")

        response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
        print("balanceRequest    : account='yl001'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")


        response = stub.deposit(bank_pb2.depositRequest(account='yl002',value=100))
        print("depositRequest    : account='yl002',value=100")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")


        response = stub.transfer(bank_pb2.transferRequest(fromAccount='yl001',toAccount='yl002',value=100))
        print("transferRequest   : fromAccount='yl001',toAccount='yl002',value=100")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")


        response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
        print("balanceRequest    : account='yl001'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")


        response = stub.balance(bank_pb2.balanceRequest(account='yl002'))
        print("balanceRequest    : account='yl002'")
        print("received          : " + response.message + ", " +str(response.balance));
        print("-------------------------------------------")

        #
        # responses = stub.getRecord(bank_pb2.getRecordRequest(account='yl001'))
        # print("getRecordRequest  : account='yl001'")
        # for response in responses:
        #     print("received          : " + response.account + ", " +str(response.value)+ ", " +str(response.time));
        # print("-------------------------------------------")



if __name__ == '__main__':
    # run()
    # 创建 10 个线程
    # thrs1 = [threading.Thread(target=run1000_1) for i in range(1)]
    # # 开始执行线程
    # [thr.start() for thr in thrs1]
    # 等待线程结束

    # thrs2 = [threading.Thread(target=run1000_2) for i in range(5)]
    # # 开始执行线程
    # [thr.start() for thr in thrs2]
    # # 等待线程结束
    #
    # thrs3 = [threading.Thread(target=run1000_3) for i in range(5)]
    # # 开始执行线程
    # [thr.start() for thr in thrs3]
    #
    # thrs4 = [threading.Thread(target=run1000_4) for i in range(5)]
    # # 开始执行线程
    # [thr.start() for thr in thrs4]

    # 等待线程结束
    # [thr.join() for thr in thrs1]

    # # 等待线程结束
    # [thr.join() for thr in thrs2]
    #
    # # 等待线程结束
    # [thr.join() for thr in thrs3]
    #
    # # 等待线程结束
    # [thr.join() for thr in thrs4]

    getRecord()