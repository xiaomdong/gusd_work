import log
g_log=log.getLogging(__name__)

import sys
from eth_account.messages import defunct_hash_message

sys.path.append("../../gusd_work")
sys.path.append("../../gusd_work/bank")
sys.path.append("../../gusd_work/eth")

from eth.eth_interface import *
from eth import deploy_dollor
from web3.middleware import geth_poa_middleware

# import bank.bank_pb2_grpc as bank_pb2_grpc

from bank import bank_pb2_grpc
from bank import bank_pb2

import grpc
import threading

BANK_SERVER = '172.16.1.176:50052'
BANK_CLIENT = None

ETH_NODE_SERVER="http://127.0.0.1:8545"

REGULATORY_BANK_ACCOUNT = "GEMINI_REGULATORY"  # 监管账户
COLLECTIVE_BANK_ACCOUNT = "GEMINI_COLLECTIVE"  # 归集账户
SWEEPER_ETH_ACCOUNT = '0xa8512Eab06Ed25F8452Bf7A99E5C65135f822bF3'  # sweeper账户
SWEEPER_ETH_PASSWORD='123456'
ACCOUNT_ETH_PASSWORD='123456'

Custodian1Contract_address = '0x1087aB99F519798A2c7F2CEF6a42f9274F64D641'
Custodian2Contract_address = '0xe0526B779D6F326a28156809e24c894AE455CbBD'
ERC20ImplContract_address = '0x5Fd0B7Ab187773cCbAe3FA87a14B13745A602165'
ERC20StoreContract_address = '0x4c8538fAB25417B225e03441b52736Ff9Ed65295'
ERC20ProxyContract_address = '0x12E8F1F738E5E6124A2883A0f55d48bA6A355e82'
PrintLimiterContract_address = '0x4f4399DDe7687794B141254A34Dd862891ACa1B6'

Custodian1Contract = None
Custodian2Contract = None
ERC20ImplContract = None  # 他的监管人指向PrintLimiterContract
ERC20StoreContract = None  # 他的监管人指向Custodian2Contract_address
ERC20ProxyContract = None  # 他的监管人指向Custodian2Contract_address
PrintLimiterContract = None  # 他的监管人指向Custodian1Contract_address

# d34eeaea22537317145d9a29352db6c1cfa8493f 的私钥 0x81e36dfae9f79f72b63246e51e189859da4241849cb266c1abc8c16d6e3b389e
# a8512eab06ed25f8452bf7a99e5c65135f822bf3 的私钥 0x3e402e9aadfa36894659463a435f9167c9222e8c8ce910a1707df9392d496679
# a92ac0e022f5a4e3ea53d868ce2f9aeda1cf2989 的私钥 0xe190626c281b31747956178c088785723b8d8dbbd7810b33d180b6c42358ea5a


g_web3 = None
# 向归集账户存入初始发行量的USD
# 通过归集账户向监管账户转账初始发行量的USD
# 设置GUSD的发行量
# 向sweeper账户发行初始GUSD

eventFilterDic = {'PrintingLocked': None}

burnGUSDRecordfun=None
printGUSDRecordfun=None
depositUSD2RegulatoryRecordfun=None
withdrawalUSD2CollectionRecordfun=None

def setEventRecordFun(burnGUSDRecordfun_,printGUSDRecordfun_,depositUSD2RegulatoryRecordfun_,withdrawalUSD2CollectionRecordfun_):
    burnGUSDRecordfun=burnGUSDRecordfun_
    printGUSDRecordfun=printGUSDRecordfun_
    depositUSD2RegulatoryRecordfun=depositUSD2RegulatoryRecordfun_
    withdrawalUSD2CollectionRecordfun=withdrawalUSD2CollectionRecordfun_

#初始化函数，设置GUSD的合约对象
def gusd_init():
    global Custodian1Contract
    global Custodian2Contract
    global ERC20ImplContract
    global ERC20StoreContract
    global ERC20ProxyContract
    global PrintLimiterContract
    global g_web3
    global g_log

    g_log.info("gusd_init run start")

    web3 = connectCanacheHTTPWeb3(ETH_NODE_SERVER)

    web3.middleware_stack.inject(geth_poa_middleware, layer=0)

    Custodian1Contract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.CUSTODIAN_FILE_PATH, 'Custodian',
                                                         Custodian1Contract_address)

    Custodian2Contract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.CUSTODIAN_FILE_PATH, 'Custodian',
                                                         Custodian2Contract_address)

    ERC20ImplContract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.ERC20IMPL_FILE_PATH, 'ERC20Impl',
                                                        ERC20ImplContract_address)

    ERC20StoreContract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.ERC20STORE_FILE_PATH, 'ERC20Store',
                                                         ERC20StoreContract_address)

    ERC20ProxyContract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.ERC20PROXY_FILE_PATH, 'ERC20Proxy',
                                                         ERC20ProxyContract_address)

    PrintLimiterContract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.PRINTLIMITER_FILE_PATH, 'PrintLimiter',
                                                           PrintLimiterContract_address)

    g_log.info("Custodian1Contract  :" + str(Custodian1Contract)   + ": address: " + Custodian1Contract_address)
    g_log.info("Custodian2Contract  :" + str(Custodian2Contract)   + ": address: " + Custodian2Contract_address)
    g_log.info("ERC20ImplContract   :" + str(ERC20ImplContract)    + ": address: " + ERC20ImplContract_address)
    g_log.info("ERC20StoreContract  :" + str(ERC20StoreContract)   + ": address: " + ERC20StoreContract_address)
    g_log.info("ERC20ProxyContract  :" + str(ERC20ProxyContract)   + ": address: " + ERC20ProxyContract_address)
    g_log.info("PrintLimiterContract:" + str(PrintLimiterContract) + ": address: " + PrintLimiterContract_address)
    g_log.info("web3:" + str(web3) + ": address: " + ETH_NODE_SERVER)
    g_log.info("gusd_init run end")
    g_log.info("------------------------------------------------")

    g_web3 = web3


#创建一个eth账户
def create_eth_addr():
    web3 = g_web3
    try:
        address=web3.personal.newAccount(ACCOUNT_ETH_PASSWORD)
        g_log.info(address)
        g_log.info(type(address))

        #为了测试方便，向每个帐号上转10个eth，用于支付gas
        web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
        txhash=web3.eth.sendTransaction(
            {'to': address, 'from': SWEEPER_ETH_ACCOUNT, 'value': web3.toWei(10,"ether")})

        web3.eth.waitForTransactionReceipt(txhash)
        return address
    except Exception as e:
        g_log.error("something err:%s" % (e))
        return None

# 获取地址的GUSD余额
def getGUSDBalance(addr):
    web3 = g_web3
    try:
        balance=ERC20ProxyContract.functions.balanceOf(addr).call()
        g_log.info(addr +" GUSD balance:" + str(balance))
        return balance
    except Exception as e:
        g_log.error("something err:%s" % (e))
        return None

# sweeper地址向其他地址转账
def sweeperTransfer(addr,value):

    web3 = g_web3
    try:
        web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
        txhash =ERC20ProxyContract.functions.transfer(addr,value).transact({'from': SWEEPER_ETH_ACCOUNT})
        web3.eth.waitForTransactionReceipt(txhash)
        g_log.info("sweeper send " + str(value) + " GUSD to " + addr)
        return txhash
    except Exception as e:
        g_log.info("sweeper send " + str(value) + " GUSD to " + addr)
        g_log.error("something err:%s" % (e))
        return None

# 向sweeper地址转账
def transferToSweeper(addr,value):
    web3 = g_web3
    try:
        web3.personal.unlockAccount(addr, ACCOUNT_ETH_PASSWORD)
        txhash =ERC20ProxyContract.functions.transfer(SWEEPER_ETH_ACCOUNT,value).transact({'from': addr})
        web3.eth.waitForTransactionReceipt(txhash)
        g_log.info(addr + " send " + str(value) + " GUSD to sweeper")
        return txhash
    except Exception as e:
        g_log.info(addr + " send " + str(value) + " GUSD to sweeper")
        g_log.error("something err:%s" % (e))
        return None

# 客户提现GUSD
def transfer(fromaddr,toaddr,value):
    web3 = g_web3
    try:
        web3.personal.unlockAccount(fromaddr, ACCOUNT_ETH_PASSWORD)
        txhash =ERC20ProxyContract.functions.transfer(toaddr,value).transact({'from': fromaddr})
        web3.eth.waitForTransactionReceipt(txhash)
        g_log.info(fromaddr + " send " + str(value) + " GUSD to " + toaddr)
        return txhash
    except Exception as e:
        g_log.info(fromaddr + " send " + str(value) + " GUSD to " + toaddr)
        g_log.error("something err:%s" % (e))
        return None

# # 测试接口，转账gusd
# def transfer(fromaddr,password, toaddr,value):
#     web3 = g_web3
#     try:
#         web3.personal.unlockAccount(fromaddr, password)
#         txhash =ERC20ProxyContract.functions.transfer(toaddr,value).transact({'from': fromaddr})
#         web3.eth.waitForTransactionReceipt(txhash)
#         g_log.info(fromaddr + " send " + str(value) + " GUSD to " + toaddr)
#         return txhash
#     except Exception as e:
#         g_log.info(fromaddr + " send " + str(value) + " GUSD to " + toaddr)
#         g_log.error("something err:%s" % (e))
#         return None

#获取银行账户余额
def bankBlance(account_):
    try:
        with grpc.insecure_channel(BANK_SERVER) as channel:
            stub = bank_pb2_grpc.bankStub(channel)

            response = stub.balance(
                bank_pb2.balanceRequest(account=account_))

            if (response.message != 'OK'):
                return None

            g_log.info(account_ + " bank balance:" + str(response.balance))
            return response.balance
    except Exception as e:
        g_log.error("something err:%s" % (e))
        return None

def bankTransfer(fromAccount_,toAccount_,value_):
    try:
        with grpc.insecure_channel(BANK_SERVER) as channel:
            stub = bank_pb2_grpc.bankStub(channel)

            response = stub.transfer(
                bank_pb2.transferRequest(fromAccount=fromAccount_,toAccount=toAccount_,value=value_))
            # print("received          : " + response.message + ", " + str(response.balance));
            g_log.info(fromAccount_ + " send " + str(value_) +" usd to "+ toAccount_)

            if(response.message != 'OK'):
                return None

            return response
    except Exception as e:
        g_log.info(fromAccount_ + "send " + str(value_) + " usd to " + toAccount_)
        g_log.error("something err:%s" % (e))
        return None

#从归集账户向监管账户转账
#发行GUSD
# def gusd_print(money):
#     web3 = g_web3
#     with grpc.insecure_channel(BANK_SERVER) as channel:
#         stub = bank_pb2_grpc.bankStub(channel)
#
#         response = stub.deposit(
#             bank_pb2.balance(account=COLLECTIVE_BANK_ACCOUNT))
#         print("received          : " + response.message + ", " + str(response.balance));
#
#         if(response.balance <= money):
#             print("Insufficient account balance!!!")
#             return None
#
#         response = stub.deposit(
#             bank_pb2.transferRequest(fromAccount=COLLECTIVE_BANK_ACCOUNT, toAccount=REGULATORY_BANK_ACCOUNT,
#                                      value=money))
#         print("received          : " + response.message + ", " + str(response.balance));
#
#         web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
#         txhash=PrintLimiterContract.functions.limitedPrint(SWEEPER_ETH_ACCOUNT, money).transact({'from': SWEEPER_ETH_ACCOUNT})
#         web3.eth.waitForTransactionReceipt(txhash)

def gusd_print(money):
    web3 = g_web3

    balance=bankBlance(COLLECTIVE_BANK_ACCOUNT)
    if(balance==None):
        return None

    if(balance <= money):
        g_log.error("Insufficient account balance!!!: "+str(balance)+" < "+str(money))
        return None

    result=bankTransfer(COLLECTIVE_BANK_ACCOUNT,REGULATORY_BANK_ACCOUNT,money) #result.recordIndex
    if(result ==None):
        return None

    if(depositUSD2RegulatoryRecordfun!=None):
        depositUSD2RegulatoryRecordfun(money, result.recordIndex)
    try:
        web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
        txhash=PrintLimiterContract.functions.limitedPrint(SWEEPER_ETH_ACCOUNT, money).transact({'from': SWEEPER_ETH_ACCOUNT})
        web3.eth.waitForTransactionReceipt(txhash)
        g_log.info("print " + str(money) +" GUSD")
        return txhash
    except Exception as e:
        #这里出现错误要尝试操作，如果尝试不成功，需要回退，待添加
        g_log.error("something err:%s" % (e))
        return None

#获取GUSD发行量
def get_gusd_print():
    web3 = g_web3
    try:
        gusdPrint=ERC20ProxyContract.functions.totalSupply().call()

        g_log.info("total print " + str(gusdPrint) +" GUSD")
        return gusdPrint
    except Exception as e:
        #这里出现错误要尝试操作，如果尝试不成功，需要回退，待添加
        g_log.error("something err:%s" % (e))
        return None



#从监管账户归集账户转账
#燃烧GUSD
# def gusd_burn(money):
#     web3 = g_web3
#     with grpc.insecure_channel(BANK_SERVER) as channel:
#         stub = bank_pb2_grpc.bankStub(channel)
#
#         response = stub.deposit(
#             bank_pb2.balance(account=REGULATORY_BANK_ACCOUNT))
#         print("REGULATORY_BANK_ACCOUNT          balance: " + response.message + ", " + str(response.balance));
#
#         if(response.balance <= money):
#             print("Insufficient account balance!!!")
#             return None
#
#         response = stub.deposit(
#             bank_pb2.transferRequest(fromAccount=REGULATORY_BANK_ACCOUNT, toAccount=COLLECTIVE_BANK_ACCOUNT,
#                                      value=money))
#         print("REGULATORY_BANK_ACCOUNT transfer COLLECTIVE_BANK_ACCOUNT: " + response.message + ", " + str(response.balance));
#
#         web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, "123456")
#         txhash = ERC20ImplContract.functions.burn(money).transact({'from': SWEEPER_ETH_ACCOUNT})
#         web3.eth.waitForTransactionReceipt(txhash)

def gusd_burn(money):
    web3 = g_web3

    balance = bankBlance(REGULATORY_BANK_ACCOUNT)
    if(balance == None):
        return None

    if(balance <= money):
        g_log.error("Insufficient account balance!!!: "+str(balance)+" < "+str(money))
        return None

    result=bankTransfer(REGULATORY_BANK_ACCOUNT,COLLECTIVE_BANK_ACCOUNT,money)
    if(result == None):
        return None

    if(withdrawalUSD2CollectionRecordfun != None):
        withdrawalUSD2CollectionRecordfun(money, result.recordIndex)
    try:
        web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
        txhash = ERC20ImplContract.functions.burn(money).transact({'from': SWEEPER_ETH_ACCOUNT})
        web3.eth.waitForTransactionReceipt(txhash)
        g_log.info("burn " + str(money) + " GUSD")
    except Exception as e:
        #这里出现错误要尝试操作，如果尝试不成功，需要回退，待添加
        g_log.error("something err:%s" % (e))
        return None


#在银行开户归集账户和监管账户
#向归集账户转入初始发行的USD
#从归集账户想监管账户转账初始发行的USD
#发行GUSD
def gusd_init_print(money):
    web3 = g_web3
    with grpc.insecure_channel(BANK_SERVER) as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        response = stub.deposit(bank_pb2.depositRequest(account=COLLECTIVE_BANK_ACCOUNT, value=money))
        print("COLLECTIVE_BANK_ACCOUNT          deposit: " + response.message + ", " + str(response.balance));

        response = stub.deposit(bank_pb2.depositRequest(account=REGULATORY_BANK_ACCOUNT, value=0))
        print("REGULATORY_BANK_ACCOUNT          deposit: " + response.message + ", " + str(response.balance));

        response = stub.deposit(
            bank_pb2.transferRequest(fromAccount=COLLECTIVE_BANK_ACCOUNT, toAccount=REGULATORY_BANK_ACCOUNT,
                                     value=money))
        print("COLLECTIVE_BANK_ACCOUNT transfer REGULATORY_BANK_ACCOUNT: " + response.message + ", " + str(response.balance));


        web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
        txhash = PrintLimiterContract.functions.limitedPrint(SWEEPER_ETH_ACCOUNT, money).transact({'from': SWEEPER_ETH_ACCOUNT})
        web3.eth.waitForTransactionReceipt(txhash)

        # ERC20ImplContract.functions.requestPrint(SWEEPER_ETH_ACCOUNT, money).call()

        # print(web3.toHex(ERC20ImplContract.functions.requestPrint(SWEEPER_ETH_ACCOUNT, money).transact()))

        # worker1 = threading.Thread(target=request_loop, args=(web3,), daemon=True)
        # worker1.start()

        # #转账
        # web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, "123456")
        # ERC20ProxyContract.functions.transfer("0xD34eEAea22537317145d9A29352Db6c1cfa8493f",10000).transact({'from': SWEEPER_ETH_ACCOUNT})

        # #燃烧
        # web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, "123456")
        # ERC20ImplContract.functions.burn(10000).transact({'from': SWEEPER_ETH_ACCOUNT})

        # 转移账户
        # web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, "123456")
        # print(web3.toHex(ERC20ImplContract.functions.sweepMsg().call()))

        # message_hash = defunct_hash_message(text="sweep")
        # print(message_hash)
        # print(web3.toHex(message_hash))
        # print('------------------')
        #
        # message_hash = web3.sha3(text='sweep')
        # print(message_hash)
        # print(web3.toHex(message_hash))
        # print('------------------')
        #
        #
        # message_hash = web3.soliditySha3(['address', 'string'], ["0x5Fd0B7Ab187773cCbAe3FA87a14B13745A602165", "sweep"])
        # print(message_hash)
        # print(web3.toHex(message_hash))
        # print('------------------***')

        # #ethscan 查询出来的GUSD的sweepMsg
        # #soliditySha3 与 solidity中的keccak256函数功能一致
        # message_hash = web3.soliditySha3(['address','string'],["0x6704ba24b8640BCcEe6BF2fd276a6a1b8EdF4Ade","sweep"])
        # print(message_hash)
        # print(web3.toHex(message_hash))
        # print('------------------***')

        # #获取账户私钥 d34eeaea22537317145d9a29352db6c1cfa8493f
        # #0x81e36dfae9f79f72b63246e51e189859da4241849cb266c1abc8c16d6e3b389e
        # with open('/data/eth_workspace/node0/keystore/UTC--2018-11-08T09-25-55.757410788Z--d34eeaea22537317145d9a29352db6c1cfa8493f') as keyfile:
        #     encrypted_key = keyfile.read()
        #     private_key = web3.eth.account.decrypt(encrypted_key, '123456')
        #     print(private_key)
        #     print(web3.toHex(private_key))
        #
        # print('****------------------****------------------****')
        #
        #
        # signed_message = web3.eth.account.signHash(message_hash, private_key='0x81e36dfae9f79f72b63246e51e189859da4241849cb266c1abc8c16d6e3b389e')
        # result=web3.eth.account.recoverHash(message_hash, signature=signed_message.signature)
        # print(result)
        # print('****------------------****------------------****')
        #
        #
        #
        # #获取账户私钥 a8512eab06ed25f8452bf7a99e5c65135f822bf3
        # #0x3e402e9aadfa36894659463a435f9167c9222e8c8ce910a1707df9392d496679
        # with open('/data/eth_workspace/node0/keystore/UTC--2018-11-08T09-25-09.444732434Z--a8512eab06ed25f8452bf7a99e5c65135f822bf3') as keyfile:
        #     encrypted_key = keyfile.read()
        #     private_key = web3.eth.account.decrypt(encrypted_key, '123456')
        #     print(private_key)
        #     print(web3.toHex(private_key))
        #
        # print('****------------------****------------------****')
        #
        #
        # signed_message = web3.eth.account.signHash(message_hash, private_key='0x3e402e9aadfa36894659463a435f9167c9222e8c8ce910a1707df9392d496679')
        # result=web3.eth.account.recoverHash(message_hash, signature=signed_message.signature)
        # print(result)
        # print('****------------------****------------------****')
        #

        # #获取账户私钥 a92ac0e022f5a4e3ea53d868ce2f9aeda1cf2989
        # #0xe190626c281b31747956178c088785723b8d8dbbd7810b33d180b6c42358ea5a
        # with open('/data/eth_workspace/node0/keystore/UTC--2018-11-08T09-25-36.372846840Z--a92ac0e022f5a4e3ea53d868ce2f9aeda1cf2989') as keyfile:
        #     encrypted_key = keyfile.read()
        #     private_key = web3.eth.account.decrypt(encrypted_key, '123456')
        #     print(private_key)
        #     print(web3.toHex(private_key))
        #
        # print('****------------------****------------------****')
        #
        #
        # signed_message = web3.eth.account.signHash(message_hash,
        #                                            private_key='0x3e402e9aadfa36894659463a435f9167c9222e8c8ce910a1707df9392d496679')
        # result = web3.eth.account.recoverHash(message_hash, signature=signed_message.signature)
        # print(result)
        # print('****------------------****------------------****')
        # print('****------------------****------------------****')
        # print('****------------------****------------------****')
        #
        # message_hash = ERC20ImplContract.functions.sweepMsg().call()
        # print(web3.toHex(message_hash))
        # print("0x9601a30018e754e4afb23b4a6aca77618c136b6b30a5cf92f784197c55088f16")
        # print("-------------------------------")
        # signed_message = web3.eth.account.signHash(message_hash,
        #                                            private_key='0x3e402e9aadfa36894659463a435f9167c9222e8c8ce910a1707df9392d496679')
        #
        # print(web3.eth.account.recoverHash(message_hash, signature=signed_message.signature))
        #
        # print(signed_message)
        # # print(signedData)
        # # r = signedData[0:64]
        # # s = signedData[64:128]
        # # v = signedData[128:130]
        # # print(signed_message)
        # result = ERC20ImplContract.functions.enableSweep([web3.toInt(signed_message['v'])],
        #                                                  [web3.toBytes(signed_message['r'])],
        #                                                  [web3.toBytes(signed_message['s'])],
        #                                                  "0xD34eEAea22537317145d9A29352Db6c1cfa8493f").transact(
        #     {'from': SWEEPER_ETH_ACCOUNT})
        # print(result)
        # print(web3.toHex(result))
        # # # ERC20ImplContract.functions.replaySweep([SWEEPER_ETH_ACCOUNT],"0xD34eEAea22537317145d9A29352Db6c1cfa8493f").transact({'from': SWEEPER_ETH_ACCOUNT})


#测试函数
def request_loop(web3):
    ERC20ImplContract = deploy_dollor.get_gusd_contract(web3, deploy_dollor.ERC20IMPL_FILE_PATH, 'ERC20Impl',
                                                        '0x5Fd0B7Ab187773cCbAe3FA87a14B13745A602165')
    value = 1000
    for i in range(5):
        # print(web3.toHex(ERC20ImplContract.functions.requestPrint(SWEEPER_ETH_ACCOUNT, value).transact()))
        # print("----------------------------")
        web3.personal.unlockAccount(SWEEPER_ETH_ACCOUNT, SWEEPER_ETH_PASSWORD)
        PrintLimiterContract.functions.limitedPrint(SWEEPER_ETH_ACCOUNT, value).transact({'from': SWEEPER_ETH_ACCOUNT})
        value = value + 10
        time.sleep(10)



#event处理函数
def handle_event(event):
    web3 = g_web3

    if (event['event'] == "PrintingLocked"):
        print(
            event['event'] + ":" + web3.toHex(event['args']['_lockId']) + "," + event['args']['_receiver'] + "," + str(
                event['args']['_value']))
    if (event['event'] == "PrintingConfirmed"):
        print(
            event['event'] + ":" + web3.toHex(event['args']['_lockId']) + "," + event['args']['_receiver'] + "," + str(
                event['args']['_value']))

    if (event['event'] == "Transfer"):
        # print(web3.toHex(event['transactionHash']))
        # print(type(web3.toHex(event['transactionHash'])))
        print(event['event'] + ":" + event['args']['_from'] + "," + event['args']['_to'] + "," + str(
            event['args']['_value']))

        if (event['args']['_to'] == '0x0000000000000000000000000000000000000000'):
            print("burn operation")
            if(burnGUSDRecordfun!=None):
                burnGUSDRecordfun(event['args']['_value'],web3.toHex(event['transactionHash']))

        if (event['args']['_from'] == '0x0000000000000000000000000000000000000000'):
            print("print operation")
            if(printGUSDRecordfun!=None):
                printGUSDRecordfun(event['args']['_value'],web3.toHex(event['transactionHash']))
        print("-----------------------------")

#event 循环接收
def event_loop(eventFilterDic, poll_interval):
    while True:
        for (k, v) in eventFilterDic.items():
            if (v != None):
                for event in v.get_new_entries():
                    handle_event(event)
        time.sleep(poll_interval)

def event_thread_run():
    eventFilterDic["PrintingLocked"] = ERC20ImplContract.events.PrintingLocked.createFilter(fromBlock='latest')
    eventFilterDic["PrintingConfirmed"] = ERC20ImplContract.events.PrintingConfirmed.createFilter(fromBlock='latest')
    eventFilterDic["Transfer"] = ERC20ProxyContract.events.Transfer.createFilter(fromBlock='latest')
    eventThread = threading.Thread(target=event_loop, args=(eventFilterDic, 5), daemon=True)
    eventThread.start()


if __name__ == '__main__':

    gusd_init()

    create_eth_addr()

    # gusd_init_print(100000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # bankBlance(COLLECTIVE_BANK_ACCOUNT)
    # getGUSDBalance(SWEEPER_ETH_ACCOUNT)
    # get_gusd_print()

    #
    # gusd_print(10000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_print(100)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_print(1000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_print(55555)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    #
    # gusd_print(555555)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    #
    # gusd_burn(55555)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_burn(1000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_burn(100)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_burn(10000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # bankBlance(COLLECTIVE_BANK_ACCOUNT)
    # get_gusd_print()
    #
    #
    # # eventFilterDic["PrintingLocked"] = ERC20ImplContract.events.PrintingLocked.createFilter(fromBlock='latest')
    # # eventFilterDic["PrintingConfirmed"] = ERC20ImplContract.events.PrintingConfirmed.createFilter(fromBlock='latest')
    # # eventFilterDic["Transfer"] = ERC20ProxyContract.events.Transfer.createFilter(fromBlock='latest')
    # #
    # # eventThread = threading.Thread(target=event_loop, args=(eventFilterDic, 5), daemon=True)
    # # eventThread.start()
    # event_thread_run()
    #
    # # print("==========================================")
    # # print(getGUSDBalance('0xD34eEAea22537317145d9A29352Db6c1cfa8493f'))
    # # print("==========================================")
    # #
    # # print("==========================================")
    # # print(create_eth_addr())
    # # print("==========================================")
    #
    #
    # gusd_init_print(1000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # bankBlance(COLLECTIVE_BANK_ACCOUNT)
    # get_gusd_print()
    #
    # gusd_print(10000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_print(100)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_print(1000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_print(55555)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    #
    # gusd_print(555555)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    #
    # gusd_burn(55555)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_burn(1000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_burn(100)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # get_gusd_print()
    # gusd_burn(10000)
    # bankBlance(REGULATORY_BANK_ACCOUNT)
    # bankBlance(COLLECTIVE_BANK_ACCOUNT)
    # get_gusd_print()
    #
    #
    # while (1):
    #     time.sleep(10)
