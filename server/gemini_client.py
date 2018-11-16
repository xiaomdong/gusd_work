from __future__ import print_function
import threading
import grpc

import gemini_pb2
import gemini_pb2_grpc
import control

#
# def run1000_1():
#     with grpc.insecure_channel('172.16.1.176:50052') as channel:
#         stub = gemini_pb2_grpc.geminiStub(channel)
#         for i in range(1000):
#             response = stub.deposit(gemini_pb2.depositRequest(account='yl001',value=2))
#             if (i % 100 ==0):
#                 print("run...run1000_1")
#         response = stub.balance(gemini_pb2.balanceRequest(account='yl001'))
#         print("balanceRequest    : account='yl001'")
#         print("received          : " + response.message + ", " +str(response.balance));
#         print("-------------------------------------------")
#
# def run1000_2():
#     with grpc.insecure_channel('172.16.1.176:50052') as channel:
#         stub = gemini_pb2_grpc.geminiStub(channel)
#         for i in range(1000):
#             response = stub.deposit(gemini_pb2.withdrawalRequest(account='yl001',value=1))
#             if (i % 100 ==0):
#                 print("run...run1000_2")
#
#         response = stub.balance(gemini_pb2.balanceRequest(account='yl001'))
#         print("balanceRequest    : account='yl001'")
#         print("received          : " + response.message + ", " +str(response.balance));
#         print("-------------------------------------------")
#
# def run1000_3():
#     with grpc.insecure_channel('172.16.1.176:50052') as channel:
#         stub = gemini_pb2_grpc.geminiStub(channel)
#         for i in range(1000):
#             response = stub.deposit(gemini_pb2.depositRequest(account='yl002',value=1))
#             if (i % 100 ==0):
#                 print("run...run1000_3")
#
#         response = stub.balance(gemini_pb2.balanceRequest(account='yl002'))
#         print("balanceRequest    : account='yl002'")
#         print("received          : " + response.message + ", " +str(response.balance));
#         print("-------------------------------------------")
#
#
#
# def run1000_4():
#     with grpc.insecure_channel('172.16.1.176:50052') as channel:
#         stub = gemini_pb2_grpc.geminiStub(channel)
#         for i in range(1000):
#             # response = stub.deposit(bank_pb2.depositRequest(account='yl002',value=1))
#             response = stub.transfer(gemini_pb2.transferRequest(fromAccount='yl001', toAccount='yl002', value=1))
#             if (i % 100 ==0):
#                 print("run...run1000_4")
#
#         response = stub.balance(gemini_pb2.balanceRequest(account='yl001'))
#         print("balanceRequest    : account='yl001'")
#         print("received          : " + response.message + ", " +str(response.balance));
#         print("-------------------------------------------")
#         response = stub.balance(gemini_pb2.balanceRequest(account='yl002'))
#         print("balanceRequest    : account='yl002'")
#         print("received          : " + response.message + ", " +str(response.balance));
#         print("-------------------------------------------")
#
# def getRecord():
#     with grpc.insecure_channel('172.16.1.176:50052') as channel:
#         stub = gemini_pb2_grpc.geminiStub(channel)
#         # response = stub.balance(bank_pb2.balanceRequest(account='yl001'))
#         # print(response)
#         responses = stub.getRecord(gemini_pb2.getRecordRequest(account='yl001'))
#         for response in responses:
#             print(response)
#
#         # responses = stub.getRecord(bank_pb2.getRecordRequest(account='yl001'))
#         # responses = stub.getRecord(bank_pb2.getRecordRequest(account='yl001'))
#         # print("getRecordRequest  : account='yl001'")
#         # for response in responses:
#         #     print("received          : " + response.account + ", " +str(response.value)+ ", " +str(response.time));
#         # print("-------------------------------------------")

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('172.16.1.175:50053') as channel:
        stub = gemini_pb2_grpc.geminiStub(channel)

        #钱包上的地址是 account20
        response = stub.register(gemini_pb2.registerRequest(account='genemi_yl001',
                                                            password='123456',
                                                            mail="yl001@gmail.com",
                                                            phone="00000000001",
                                                            withdrawBankAccount="bank_yl001",
                                                            withdrawEthaddress="0xB0B5Cc397ED952587a4B1A17AFDdF01F99DA4531"))

        print(response)

        response = stub.login(gemini_pb2.loginRequest(account='yl001',password='123'))
        print("depositRequest    : account='yl001',password='123'")
        print("received          : " + str(response));
        print("-------------------------------------------")

        response = stub.register(gemini_pb2.registerRequest(account='yl001',password="123",mail='xd@gmail.com',phone='18033441090',withdrawBankAccount='xd2',withdrawEthaddress='eth123'))
        print("depositRequest    : account='yl001',password='123',mail='xd@gmail.com',phone='18033441090',withdrawBankAccount='xd2',withdrawEthaddress='eth123'")
        print("received          : " + str(response));
        print("-------------------------------------------")

        response = stub.balance(gemini_pb2.balanceRequest(account='yl001'))
        print("balanceRequest : account='yl001'")
        print("received          : " + str(response));
        print("-------------------------------------------")

        response = stub.info(gemini_pb2.infoRequest(account='yl001'))
        print("infoRequest    : account='yl001'")
        print("received          : " + str(response));
        print("-------------------------------------------")


        response = stub.exchangeGUSD(gemini_pb2.exchangeGUSDRequest(account='yl002',usd=100))
        print("exchangeGUSDRequest    : account='yl002',usd=100")
        print("received          : " + str(response));
        print("-------------------------------------------")


        response = stub.exchangeUSD(gemini_pb2.exchangeUSDRequest(account='yl002',gusd=100))
        print("transferRequest   : account='yl002',gusd=100")
        print("received          : " + str(response));
        print("-------------------------------------------")


        response = stub.withdrawalUSD(gemini_pb2.withdrawalUSDRequest(account='yl002',withdrawBankAccount='xd2',usd=200))
        print("withdrawalUSDRequest    : account='yl002',withdrawBankAccount='xd2',usd=200")
        print("received          : " + str(response));
        print("-------------------------------------------")


        response = stub.withdrawalGUSD(gemini_pb2.withdrawalGUSDRequest(account='yl002',withdrawEthaddress='xd2eth',gusd=200))
        print("balanceRequest    : account='yl002',withdrawEthaddress='xd2eth',usd=200")
        print("received          : " + str(response));
        print("-------------------------------------------")


        responses = stub.record(gemini_pb2.recordRequest(account='yl001'))
        print("getRecordRequest  : account='yl001'")
        for response in responses:
            print("received          : " + str(response));
        print("-------------------------------------------")

        response = stub.bankInfo(gemini_pb2.bankInfoRequest(account='xd2',time='123123',operation=1,otherAccount='xd1',value=3,recordIndex='1'))
        print("bankInfo    : account='xd2',time='123123',operation=1,otherAccount='xd1',value=3")
        print("received    : " + str(response));
        print("-------------------------------------------")

import sys
sys.path.append("../../gusd_work")
sys.path.append("../../gusd_work/bank")
sys.path.append("../../gusd_work/eth")
from bank import bank_pb2_grpc
from bank import bank_pb2


def test():
   #  # 测试注册用户
   #  # 创建bank_yl001用户，并存入10000
   #  with grpc.insecure_channel('172.16.1.176:50052') as channel:
   #      stub = bank_pb2_grpc.bankStub(channel)
   #
   #      # 创建bank_yl001 银行用户，存款10000
   #      response = stub.deposit(bank_pb2.depositRequest(account='bank_yl001', value=10000))
   #      print("depositRequest    : account='bank_yl001',value=10000")
   #      print("received          : " + response.message + ", " + str(response.balance) + ", " + str(
   #          response.recordIndex));
   #      print("-------------------------------------------")
   #
   # # 对应创建genemi_yl001 genemi系统用户
   #  # 钱包上的地址是 account20
   #  with grpc.insecure_channel('172.16.1.175:50053') as channel:
   #      stub = gemini_pb2_grpc.geminiStub(channel)
   #
   #      response = stub.register(gemini_pb2.registerRequest(account='genemi_yl001',
   #                                                          password='123456',
   #                                                          mail="yl002@gmail.com",
   #                                                          phone="00000000001",
   #                                                          withdrawBankAccount="bank_yl001",
   #                                                          withdrawEthaddress="0xB0B5Cc397ED952587a4B1A17AFDdF01F99DA4531"))


    # # 测试注册用户
    # #创建bank_yl002用户，并存入10000
    # with grpc.insecure_channel('172.16.1.176:50052') as channel:
    #     stub = bank_pb2_grpc.bankStub(channel)
    #
    #     #创建bank_yl002 银行用户，存款10000
    #     response = stub.deposit(bank_pb2.depositRequest(account='bank_yl002',value=10000))
    #     print("depositRequest    : account='bank_yl002',value=10000")
    #     print("received          : " + response.message + ", " +str(response.balance) +", "+str(response.recordIndex));
    #     print("-------------------------------------------")
    #
    # # 对应创建genemi_yl002 genemi系统用户
    # # 钱包上的地址是 account21
    # with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #     stub = gemini_pb2_grpc.geminiStub(channel)
    #     response = stub.register(gemini_pb2.registerRequest(account='genemi_yl002',
    #                                                         password='123456',
    #                                                         mail="yl002@gmail.com",
    #                                                         phone="00000000002",
    #                                                         withdrawBankAccount="bank_yl002",
    #                                                         withdrawEthaddress="0x16DBc3D1e32002abf22E75a2131c8f64aD67d99a"))

    # # 测试注册用户
    # #创建bank_yl003用户，并存入10000
    # with grpc.insecure_channel('172.16.1.176:50052') as channel:
    #     stub = bank_pb2_grpc.bankStub(channel)
    #
    #     #创建bank_yl002 银行用户，存款10000
    #     response = stub.deposit(bank_pb2.depositRequest(account='bank_yl003',value=10000))
    #     print("depositRequest    : account='bank_yl003',value=10000")
    #     print("received          : " + response.message + ", " +str(response.balance) +", "+str(response.recordIndex));
    #     print("-------------------------------------------")
    #
    # # 对应创建genemi_yl002 genemi系统用户
    # # 钱包上的地址是 account22
    # with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #     stub = gemini_pb2_grpc.geminiStub(channel)
    #     response = stub.register(gemini_pb2.registerRequest(account='genemi_yl003',
    #                                                         password='123456',
    #                                                         mail="yl003@gmail.com",
    #                                                         phone="00000000003",
    #                                                         withdrawBankAccount="bank_yl003",
    #                                                         withdrawEthaddress="0xe3Ee16C2e8A58B2bca58B52acd9b9a43B75a6266"))


    # # 测试注册用户
    # #创建bank_yl005用户，并存入10000
    # with grpc.insecure_channel('172.16.1.176:50052') as channel:
    #     stub = bank_pb2_grpc.bankStub(channel)
    #
    #     #创建bank_yl002 银行用户，存款10000
    #     response = stub.deposit(bank_pb2.depositRequest(account='bank_yl005',value=10000))
    #     print("depositRequest    : account='bank_yl004',value=10000")
    #     print("received          : " + response.message + ", " +str(response.balance) +", "+str(response.recordIndex));
    #     print("-------------------------------------------")

    # # 对应创建genemi_yl005 genemi系统用户
    # # 钱包上的地址是 account22
    # with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #     stub = gemini_pb2_grpc.geminiStub(channel)
    #     response = stub.register(gemini_pb2.registerRequest(account='genemi_yl005',
    #                                                         password='123456',
    #                                                         mail="yl004@gmail.com",
    #                                                         phone="00000000005",
    #                                                         withdrawBankAccount="bank_yl005",
    #                                                         withdrawEthaddress="0xD48719FE67DcAE0Ed8B1C8a0731764BD412Dc44f"))

    #
    #     print(response)
    #     print("-------------------------------------------")
    #     response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
    #     print("balanceRequest : account='genemi_yl001'")
    #     print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
    #     print("-------------------------------------------")
    #
    #
    #
    # #bank_yl001银行用户向genemi归集账户转账1000
    # with grpc.insecure_channel('172.16.1.176:50052') as channel:
    #     stub = bank_pb2_grpc.bankStub(channel)
    #
    #     response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
    #     print("balanceRequest    : account=bank_yl001")
    #     print("received          : " + response.message + ", " +str(response.balance));
    #
    #
    #     response = stub.balance(bank_pb2.balanceRequest(account=control.COLLECTIVE_BANK_ACCOUNT))
    #     print("balanceRequest    : account=control.COLLECTIVE_BANK_ACCOUNT")
    #     print("received          : " + response.message + ", " +str(response.balance));
    #
    #


    # #测试USD存款
    # #bank_yl001银行用户向genemi归集账户转账1000
    # response = stub.transfer(bank_pb2.transferRequest(fromAccount='bank_yl001',toAccount=control.COLLECTIVE_BANK_ACCOUNT,value=1000))
    # print("transferRequest   : fromAccount='bank_yl001',toAccount='control.COLLECTIVE_BANK_ACCOUNT',value=100")
    # print("received          : " + response.message + ", " +str(response.balance) +", "+str(response.recordIndex));
    #
    #
    # response = stub.balance(bank_pb2.balanceRequest(account=control.COLLECTIVE_BANK_ACCOUNT))
    # print("balanceRequest    : account=control.COLLECTIVE_BANK_ACCOUNT")
    # print("received          : " + response.message + ", " +str(response.balance));
    #
    #
    # response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
    # print("balanceRequest    : account=bank_yl001")
    # print("received          : " + response.message + ", " +str(response.balance));
    # print("-------------------------------------------")


    # 测试USD提现
    # #向genemi查询genemi_yl001余额
    # with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #     stub = gemini_pb2_grpc.geminiStub(channel)
    #     response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
    #     print("balanceRequest : account='genemi_yl001'")
    #     print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
    #     print("-------------------------------------------")
    #
    #
    # #genemi_yl001用户提现1000
    # with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #     stub = gemini_pb2_grpc.geminiStub(channel)
    #     response = stub.withdrawalUSD(gemini_pb2.withdrawalUSDRequest(account='genemi_yl001',withdrawBankAccount="bank_yl001",usd=1000))
    #     print("withdrawalUSD : account='genemi_yl001' to bankAccount='bank_yl001' value=1000")
    #     print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
    #     print("-------------------------------------------")
    #
    #
    # #向genemi查询genemi_yl001余额
    # with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #     stub = gemini_pb2_grpc.geminiStub(channel)
    #     response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
    #     print("balanceRequest : account='genemi_yl001'")
    #     print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
    #     print("-------------------------------------------")
    #
    #
    # #向银行查询bank_yl001余额
    # with grpc.insecure_channel('172.16.1.176:50052') as channel:
    #     stub = bank_pb2_grpc.bankStub(channel)
    #     response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
    #     print("balanceRequest    : account=bank_yl001")
    #     print("received          : " + response.message + ", " +str(response.balance));
    #     print("-------------------------------------------")


    #测试 USD exchange GUSD
    with grpc.insecure_channel('172.16.1.175:50053') as channel:
        stub = gemini_pb2_grpc.geminiStub(channel)
        response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
        print("balanceRequest : account='genemi_yl001'")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")

        response = stub.exchangeGUSD(gemini_pb2.exchangeGUSDRequest(account='genemi_yl001',usd=100))
        print("exchangeGUSD : account='genemi_yl001' , usd=100")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")

        response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
        print("balanceRequest : account='genemi_yl001'")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")


    # 测试GUSD兑换USD
    with grpc.insecure_channel('172.16.1.175:50053') as channel:
        stub = gemini_pb2_grpc.geminiStub(channel)
        response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
        print("balanceRequest : account='genemi_yl001'")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")

        response = stub.exchangeUSD(gemini_pb2.exchangeUSDRequest(account='genemi_yl001',gusd=100))
        print("exchangeGUSD : account='genemi_yl001' , usd=100")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")

        response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
        print("balanceRequest : account='genemi_yl001'")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")


    #测试提现GUSD

    with grpc.insecure_channel('172.16.1.175:50053') as channel:
        stub = gemini_pb2_grpc.geminiStub(channel)
        response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
        print("balanceRequest : account='genemi_yl001'")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")

        response = stub.withdrawalGUSD(gemini_pb2.withdrawalGUSDRequest(account='genemi_yl001',withdrawEthaddress='0xB0B5Cc397ED952587a4B1A17AFDdF01F99DA4531',gusd=100))
        print("exchangeGUSD : account='genemi_yl001' , usd=100")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")

        response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
        print("balanceRequest : account='genemi_yl001'")
        print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
        print("-------------------------------------------")



if __name__ == '__main__':
    # control.gusd_init()
    test()


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

    # getRecord()