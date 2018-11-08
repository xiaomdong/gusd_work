from web3.auto import w3
import asyncio
from web3 import Web3
import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source

web3_=None
from web3.middleware import geth_poa_middleware

def handle_event(event):
    # print(type(event))
    print(event)
    # print(dir(event))
    # print(event.decode('utf-8'))

    # print(web3_.toBytes(event))
    print(web3_.toHex(event))
    # print(web3_.toText(event))
    # print(event['transactionHash'])
    # print(web3_.toBytes(event))
    # and whatever

async def log_loop(event_filter, poll_interval):
    while True:
        # for event in event_filter.get_new_entries():
        #     print(type(event))
        #     handle_event(event)
        # print(event_filter.get_new_entries())
        # print(event_filter.get_new_entries())
        result=event_filter.get_new_entries()
        # print(result)
        for event in result:
            # print(event)
            handle_event(event)
        await asyncio.sleep(poll_interval)

def main(event_filter):
    block_filter = web3_.eth.filter('latest')
    tx_filter = web3_.eth.filter('pending')

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2),
                log_loop(event_filter, 2)))
    finally:
        loop.close()


def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy()

    print(type(tx_hash))
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address

if __name__ == '__main__':
    web3_ = Web3(Web3.HTTPProvider("http://127.0.0.1:8545", request_kwargs={'timeout': 60}))
    web3_.eth.defaultAccount = web3_.eth.accounts[0]
    web3_.middleware_stack.inject(geth_poa_middleware, layer=0)

    contract_source_path = 'testEvent.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    # address_ = deploy_contract(web3_, contract_interface)
    abi_ = contract_interface['abi']

    contract_ = web3_.eth.contract(
        address='0xdf6dD5E45F87DA228bB9e1c4aeD2A91e272bE985',
        abi=abi_,
    )
    print(contract_.address)
    # print(dir(contract_))
    # event_filter=contract_.events.Instructor.createFilter(fromBlock='latest')
    # main(event_filter)
    # print(address_)
    # print(type(address_))
    result = contract_.functions.setInfo("xd20",100).transact()
    print(result)
    # event_filter = web3_.eth.filter({"address": address_})
    # event_filter = web3_.eth.filter({"address": '0x0269A2fB884863BDfdc7eA5f4eA8d44334489E0E'})
    # event_filter = web3_.eth.filter({"address": '0xCe6e059196d2fdac534d6338De062Ca3986F64ea'})
    # event_filter = web3_.eth.filter({"address": '0x8EF15A4dBcc103Ac27E742b085461e6779D00e8A'})
    # event_filter = web3_.eth.filter({"address": '0x98225f3910f1c3576224a51Cbef3685111632E8F'})
    # event_filter = web3_.eth.filter({"address": '0x2c5d16217a692e17447b1330a06eed2fde617a53'})


    # main(event_filter)
    # print(dir(contract_))

