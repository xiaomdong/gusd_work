import os
import unittest
import sys
sys.path.append("../../gusd_work")
sys.path.append("../../gusd_work/bank")
sys.path.append("../../gusd_work/eth")
from bank import bank_pb2_grpc
from bank import bank_pb2

import threading
import grpc

import gemini_pb2
import gemini_pb2_grpc
import control


class testGemini(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # # 测试注册用户
    # # 创建银行账户bank_yl001，并存入10000 USD
    # # 对应创建genemi_yl001用户
    # def test_add_new_user(self):
    #     with grpc.insecure_channel('172.16.1.176:50052') as channel:
    #         stub = bank_pb2_grpc.bankStub(channel)
    #
    #         # 创建bank_yl001 银行用户，存款10000
    #         response = stub.deposit(bank_pb2.depositRequest(account='bank_yl001', value=10000))
    #         print("depositRequest    : account='bank_yl001',value=10000")
    #         print("received          : " + response.message + ", " + str(response.balance) + ", " + str(
    #             response.recordIndex));
    #         print("-------------------------------------------")
    #
    #         self.assertEqual(response.message,"OK")
    #
    #     # 对应创建genemi_yl001 genemi系统用户
    #     # 钱包上的地址是 account20
    #     with grpc.insecure_channel('172.16.1.175:50053') as channel:
    #         stub = gemini_pb2_grpc.geminiStub(channel)
    #
    #         response = stub.register(gemini_pb2.registerRequest(account='genemi_yl001',
    #                                                             password='123456',
    #                                                             mail="yl002@gmail.com",
    #                                                             phone="00000000001",
    #                                                             withdrawBankAccount="bank_yl001",
    #
    #                                                             withdrawEthaddress="0xB0B5Cc397ED952587a4B1A17AFDdF01F99DA4531"))
    #         self.assertEqual(response.message, "OK")


    #测试向genemi系统Deposit USD
    #bank_yl001银行用户向genemi归集账户转账1000 USD
    def test_DepositUSD(self):
        gusd=0
        usd =0
        gemini_usd=0
        gemini_user_usd=0
        gemini_user_gusd = 0

        #向genemi查询genemi_yl001余额
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            print("-------------------------------------------")
            gemini_user_usd=response.usd
            gemini_user_gusd=response.gusd
            self.assertEqual(response.message, "OK")

        with grpc.insecure_channel('172.16.1.176:50052') as channel:
            stub = bank_pb2_grpc.bankStub(channel)

            #查询bank_yl001银行账户balance
            response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
            print("balanceRequest    : account=bank_yl001")
            print("received          : " + response.message + ", " +str(response.balance));
            usd = response.balance
            self.assertEqual(response.message, "OK")

            #查询COLLECTIVE_BANK_ACCOUNT银行账户balance
            response = stub.balance(bank_pb2.balanceRequest(account=control.COLLECTIVE_BANK_ACCOUNT))
            print("balanceRequest    : account=control.COLLECTIVE_BANK_ACCOUNT")
            print("received          : " + response.message + ", " +str(response.balance));
            gemini_usd=response.balance
            self.assertEqual(response.message, "OK")

            #测试USD存款
            #bank_yl001银行用户向genemi归集账户转账1000
            response = stub.transfer(bank_pb2.transferRequest(fromAccount='bank_yl001',toAccount=control.COLLECTIVE_BANK_ACCOUNT,value=1000))
            print("transferRequest   : fromAccount='bank_yl001',toAccount='control.COLLECTIVE_BANK_ACCOUNT',value=1000")
            print("received          : " + response.message + ", " +str(response.balance) +", "+str(response.recordIndex));
            self.assertEqual(response.message, "OK")

            # 查询bank_yl001银行账户balance
            response = stub.balance(bank_pb2.balanceRequest(account=control.COLLECTIVE_BANK_ACCOUNT))
            print("balanceRequest    : account=control.COLLECTIVE_BANK_ACCOUNT")
            print("received          : " + response.message + ", " +str(response.balance));
            self.assertEqual(response.message, "OK")
            self.assertEqual(response.balance,gemini_usd+1000)

            #查询COLLECTIVE_BANK_ACCOUNT银行账户balance
            response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
            print("balanceRequest    : account=bank_yl001")
            print("received          : " + response.message + ", " +str(response.balance));
            self.assertEqual(response.message, "OK")
            self.assertEqual(response.balance, usd-1000)

        #向genemi查询genemi_yl001余额
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            print("-------------------------------------------")
            self.assertEqual(response.message, "OK")
            self.assertEqual(response.usd, gemini_user_usd + 1000)
            self.assertEqual(response.gusd, gemini_user_gusd)


    #测试USD提现 1000 USD
    #向genemi查询genemi_yl001余额
    def test_WithdrawalUSD(self):
        gusd=0
        usd =0
        gemini_usd=0
        gemini_user_usd=0
        gemini_user_gusd = 0
        bank_usd=0
        #从gemini系统查询genemi_yl001的USD余额
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            print("-------------------------------------------")
            gemini_user_usd = response.usd
            gemini_user_gusd = response.gusd
            self.assertEqual(response.message, "OK")

        #向银行查询bank_yl001余额
        with grpc.insecure_channel('172.16.1.176:50052') as channel:
            stub = bank_pb2_grpc.bankStub(channel)
            response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
            print("balanceRequest    : account=bank_yl001")
            print("received          : " + response.message + ", " +str(response.balance));
            bank_usd=response.balance
            print("-------------------------------------------")
            self.assertEqual(response.message, "OK")

        #从gemini系统genemi_yl001用户提现1000到bank_yl001
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.withdrawalUSD(gemini_pb2.withdrawalUSDRequest(account='genemi_yl001',withdrawBankAccount="bank_yl001",usd=1000))
            print("withdrawalUSD : account='genemi_yl001' to bankAccount='bank_yl001' value=1000")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            print("-------------------------------------------")
            self.assertEqual(response.message, "OK")

        #向genemi查询genemi_yl001余额
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            print("-------------------------------------------")
            self.assertEqual(response.usd, gemini_user_usd-1000)
            self.assertEqual(response.gusd, gemini_user_gusd)
            self.assertEqual(response.message, "OK")

        #向银行查询bank_yl001余额
        with grpc.insecure_channel('172.16.1.176:50052') as channel:
            stub = bank_pb2_grpc.bankStub(channel)
            response = stub.balance(bank_pb2.balanceRequest(account="bank_yl001"))
            print("balanceRequest    : account=bank_yl001")
            print("received          : " + response.message + ", " +str(response.balance));
            self.assertEqual(response.balance, bank_usd + 1000)
            print("-------------------------------------------")
            self.assertEqual(response.message, "OK")

    # 测试 USD exchange GUSD
    def test_ExchangeGUSD(self):
        gemini_user_usd = 0
        gemini_user_gusd = 0
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : " + response.message + ", USD:" + str(response.usd) + ", GUSD:" + str(
                response.gusd));
            gemini_user_usd=response.usd
            gemini_user_gusd=response.gusd
            self.assertEqual(response.message, "OK")

            response = stub.exchangeGUSD(gemini_pb2.exchangeGUSDRequest(account='genemi_yl001', usd=100))
            print("exchangeGUSD : account='genemi_yl001' , usd=100")
            print("received          : " + response.message + ", USD:" + str(response.usd) + ", GUSD:" + str(
                response.gusd));
            self.assertEqual(response.message, "OK")

            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : " + response.message + ", USD:" + str(response.usd) + ", GUSD:" + str(
                response.gusd));
            self.assertEqual(response.usd+response.gusd, gemini_user_usd+gemini_user_gusd)
            self.assertEqual(response.usd , gemini_user_usd -100)
            self.assertEqual(response.gusd, gemini_user_gusd+100)
            self.assertEqual(response.message, "OK")
            print("-------------------------------------------")


    # 测试GUSD兑换USD
    def test_ExchangeUSD(self):
        gemini_user_usd = 0
        gemini_user_gusd = 0
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            gemini_user_usd = response.usd
            gemini_user_gusd = response.gusd
            self.assertEqual(response.message, "OK")

            response = stub.exchangeUSD(gemini_pb2.exchangeUSDRequest(account='genemi_yl001',gusd=100))
            print("exchangeGUSD : account='genemi_yl001' , usd=100")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            self.assertEqual(response.message, "OK")

            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            self.assertEqual(response.usd + response.gusd, gemini_user_usd + gemini_user_gusd)
            self.assertEqual(response.usd , gemini_user_usd + 100)
            self.assertEqual(response.gusd, gemini_user_gusd - 100)
            self.assertEqual(response.message, "OK")
            print("-------------------------------------------")


    #测试存款GUSD
    def test_DepositGUSD(self):
        gusd_1 = 0
        gusd_2 = 0

        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.info(gemini_pb2.infoRequest(account='genemi_yl001'))
            self.assertEqual(response.message, "OK")

        control.gusd_init()
        gusd_1 = control.getGUSDBalance(control.SWEEPER_ETH_ACCOUNT)
        self.assertNotEqual(gusd_1 , None)

        gusd_2 = control.getGUSDBalance(response.depositEthaddress)
        self.assertNotEqual(gusd_2 , None)

        result=control.transfer(control.SWEEPER_ETH_ACCOUNT,response.depositEthaddress,1000)
        self.assertNotEqual(result , None)

        result = control.getGUSDBalance(control.SWEEPER_ETH_ACCOUNT)
        self.assertNotEqual(result , None)
        self.assertEqual(result , gusd_1 - 1000)

        result = control.getGUSDBalance(response.depositEthaddress)
        self.assertNotEqual(gusd_2 , None)
        self.assertEqual(result, gusd_2 + 1000)


    #测试提现GUSD
    def test_WithdrawalGUSD(self):
        gemini_user_usd = 0
        gemini_user_gusd = 0
        with grpc.insecure_channel('172.16.1.175:50053') as channel:
            stub = gemini_pb2_grpc.geminiStub(channel)
            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            gemini_user_usd = response.usd
            gemini_user_gusd = response.gusd
            self.assertEqual(response.message, "OK")

            response = stub.withdrawalGUSD(gemini_pb2.withdrawalGUSDRequest(account='genemi_yl001',withdrawEthaddress='0xB0B5Cc397ED952587a4B1A17AFDdF01F99DA4531',gusd=100))
            print("withdrawalGUSD : account='genemi_yl001' , usd=100")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));
            self.assertEqual(response.message, "OK")

            response = stub.balance(gemini_pb2.balanceRequest(account='genemi_yl001'))
            print("balanceRequest : account='genemi_yl001'")
            print("received          : "+response.message + ", USD:"+str(response.usd) +", GUSD:"+str(response.gusd));

            self.assertEqual(response.usd, gemini_user_usd)
            self.assertEqual(response.gusd, gemini_user_gusd-100)
            self.assertEqual(response.message, "OK")
            print("-------------------------------------------")