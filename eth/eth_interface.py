from web3.auto import w3
import asyncio
from web3 import Web3
import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source,compile_files
from web3.middleware import geth_poa_middleware





# 合约处理函数
def handle_event(event):
    print(event)


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

# 合约时间处理
def main(event_filter_):
    # block_filter = web3_.eth.filter('latest')
    # tx_filter = web3_.eth.filter('pending')

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2),
                log_loop(event_filter_, 2)))
    finally:
        loop.close()

# 编译sol合约代码
def compile_source(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)


def compile_file(file_path):
    return compile_files([file_path])

# 部署合约
def deploy_contract(web3, contract_interface):
    tx_hash = web3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    address = tx_receipt['contractAddress']
    return address

# 部署合约，带构造函数参数
def deploy_contract_with_args(web3, contract_interface,*args_):
    tx_hash = web3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy(args=list(args_))
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    address = tx_receipt['contractAddress']
    return address

def connectHTTPWeb3(url):
    web3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 60}))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    web3.personal.unlockAccount(web3.eth.accounts[0],"123456")
    web3.middleware_stack.inject(geth_poa_middleware, layer=0) #poc链
    return web3

def connectCanacheHTTPWeb3(url):
    web3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 60}))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    web3.personal.unlockAccount(web3.eth.accounts[0],"123456")
    # web3.middleware_stack.inject(geth_poa_middleware, layer=0) #poc链
    return web3


def step1(web3):
    contract_source_path = 'testEvent.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()

    address = deploy_contract(web3, contract_interface)
    print(address)

# 将step1得到的address填写到address中
def step2(web3):
    contract_source_path = 'testEvent.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']

    contract = web3.eth.contract(
        address='0xdf6dD5E45F87DA228bB9e1c4aeD2A91e272bE985',
        abi=abi,
    )
    return contract

if __name__ == '__main__':
    web3=connectHTTPWeb3("http://127.0.0.1:8545")
    # step1()
    contract_= step2(web3)
    event_filter=contract_.events.Instructor.createFilter(fromBlock='latest')
    main(event_filter)
