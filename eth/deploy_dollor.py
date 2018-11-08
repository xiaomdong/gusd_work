from eth_interface import *


def deploy_custodian_contract(web3,*args):
    contract_source_path = './dollor/Custodian.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    address = deploy_contract_with_args(web3, contract_interface,*args)
    print(address)

if __name__ == '__main__':
    web3=connectCanacheHTTPWeb3("http://127.0.0.1:7545")
    print(web3.eth.accounts)

    deploy_custodian_contract(web3,['0xb0B0536F6FE2e6D0c611a16F7F5e6717B9bb6C12', '0x335de6AFAdD5d5adF4EE97787B48470A8cED4912'],3600,86400,'0x06f81141909619a79D0F7F46e5d9F35419eaacF1')
