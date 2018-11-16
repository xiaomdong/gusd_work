import log
g_log=None
g_log=log.getLogging()

import sys
sys.path.append("/home/test/PycharmProjects/gusd_work/server")

import grpc
from server import gemini_pb2
from server import gemini_pb2_grpc

GEMINI_SERVER = '172.16.1.175:50053'
REGULATORY_BANK_ACCOUNT = "GEMINI_REGULATORY"  # 监管账户
COLLECTIVE_BANK_ACCOUNT = "GEMINI_COLLECTIVE"  # 归集账户


def bankInfo(account_, time_, operation_, otherAccount_, value_, recordIndex_):
    if (account_ == REGULATORY_BANK_ACCOUNT
            or account_ == COLLECTIVE_BANK_ACCOUNT
            or otherAccount_ == REGULATORY_BANK_ACCOUNT
            or otherAccount_ == COLLECTIVE_BANK_ACCOUNT):
        try:
            with grpc.insecure_channel(GEMINI_SERVER) as channel:
                stub = gemini_pb2_grpc.geminiStub(channel)
                response = stub.bankInfo(gemini_pb2.bankInfoRequest(
                    account=account_,
                    time=time_,
                    operation=operation_,
                    otherAccount=otherAccount_,
                    value=value_,
                    recordIndex=recordIndex_))

                g_log.info("bankInfo to  GEMINI_SERVER: %s" % (response.message))
        except Exception as e:
            g_log.error("something err:%s" % (e))


# def bankInfo(account_, time_, operation_, otherAccount_, value_, recordIndex_):
#     if (account_ == REGULATORY_BANK_ACCOUNT
#             or account_ == COLLECTIVE_BANK_ACCOUNT
#             or otherAccount_ == REGULATORY_BANK_ACCOUNT
#             or otherAccount_ == COLLECTIVE_BANK_ACCOUNT):
#         # try:
#         with grpc.insecure_channel(GEMINI_SERVER) as channel:
#             stub = gemini_pb2_grpc.geminiStub(channel)
#             response = stub.bankInfo(gemini_pb2.bankInfoRequest(
#                 account=account_,
#                 time=time_,
#                 operation=operation_,
#                 otherAccount=otherAccount_,
#                 value=value_,
#                 recordIndex=recordIndex_))
#
#             g_log.info("bankInfo to  GEMINI_SERVER: %s" % (response.message))
#         # except Exception as e:
#         #     g_log.error("something err:%s" % (e))
