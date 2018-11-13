from eth_interface import *
from web3.middleware import geth_poa_middleware

# CUSTODIAN_FILE_PATH    = './dollor/Custodian.sol'
# ERC20STORE_FILE_PATH   = './dollor/ERC20Store.sol'
# ERC20PROXY_FILE_PATH   = './dollor/ERC20Proxy.sol'
# ERC20IMPL_FILE_PATH    = './dollor/ERC20Impl.sol'
# PRINTLIMITER_FILE_PATH = './dollor/PrintLimiter.sol'
# DEPLOY_FILE_PATH       = './dollor/deploy.sol'

CUSTODIAN_FILE_PATH    = '/home/test/PycharmProjects/gusd_work/eth/dollor/Custodian.sol'
ERC20STORE_FILE_PATH   = '/home/test/PycharmProjects/gusd_work/eth/dollor/ERC20Store.sol'
ERC20PROXY_FILE_PATH   = '/home/test/PycharmProjects/gusd_work/eth/dollor/ERC20Proxy.sol'
ERC20IMPL_FILE_PATH    = '/home/test/PycharmProjects/gusd_work/eth/dollor/ERC20Impl.sol'
PRINTLIMITER_FILE_PATH = '/home/test/PycharmProjects/gusd_work/eth/dollor/PrintLimiter.sol'
DEPLOY_FILE_PATH       = '/home/test/PycharmProjects/gusd_work/eth/dollor/deploy.sol'

# def deploy_gusd_contract(web3,path,constractName,*args):
#     contract_source_path = path
#     compiled_sol = compile_file(contract_source_path)
#     contract_interface=compiled_sol[path+":"+constractName]
#     address = deploy_contract_with_args(web3, contract_interface,*args)
#     return address


def deploy_gusd_contract(web3,path,constractName,*args):
    contract_source_path = path
    compiled_sol = compile_file(contract_source_path)
    contract_interface=compiled_sol[path+":"+constractName]
    address_ = deploy_contract_with_args(web3, contract_interface,*args)

    contract = web3.eth.contract(
        address=address_,
        abi=contract_interface['abi'],
    )
    # print(dir(contract))
    return contract

def get_gusd_contract(web3,path,constractName,address_,*args):
    contract_source_path = path
    compiled_sol = compile_file(contract_source_path)
    # print(compiled_sol.keys())
    contract_interface=compiled_sol[path+":"+constractName]
    # address_ = deploy_contract_with_args(web3, contract_interface,*args)

    contract = web3.eth.contract(
        address=address_,
        abi=contract_interface['abi'],
    )
    # print(dir(contract))
    return contract



if __name__ == '__main__':

    # for Ganache
    # web3=connectCanacheHTTPWeb3("http://127.0.0.1:7545")
    # print(web3.eth.accounts)
    #
    # _sweeper = '0x06f81141909619a79D0F7F46e5d9F35419eaacF1'
    #
    # signer1 = '0xb0B0536F6FE2e6D0c611a16F7F5e6717B9bb6C12'  #私钥是ccb2a9f96a56c21c7eb73467876b141aaa9ccb857abf422f0aba203f858954cc
    # signer2 = '0x335de6AFAdD5d5adF4EE97787B48470A8cED4912'  #私钥是193b422de71590277ef2b2035045cfb7d9eb9743d004ab8c15c5e9f0d1bc9d4a


    # #for true eth private net
    # web3=connectCanacheHTTPWeb3("http://127.0.0.1:8545")
    # print(web3.eth.accounts)
    # web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    #
    # _sweeper = '0xa8512Eab06Ed25F8452Bf7A99E5C65135f822bF3'
    #
    # signer1 = '0xa92ac0e022f5a4e3eA53D868CE2F9AEDA1Cf2989'  #0xe190626c281b31747956178c088785723b8d8dbbd7810b33d180b6c42358ea5a
    # signer2 = '0xD34eEAea22537317145d9A29352Db6c1cfa8493f'  #0x81e36dfae9f79f72b63246e51e189859da4241849cb266c1abc8c16d6e3b389e
    # _defaultTimeLock  = 3600
    # _extendedTimeLock = 86400
    # _primary = _sweeper
    #
    # #第一步，部署Custodian 合约实例 1
    # #_signers=['0xb0B0536F6FE2e6D0c611a16F7F5e6717B9bb6C12', '0x335de6AFAdD5d5adF4EE97787B48470A8cED4912']
    # #_defaultTimeLock=3600
    # # _extendedTimeLock = 86400
    # #_primary=0x06f81141909619a79D0F7F46e5d9F35419eaacF1
    # Custodian1 = deploy_gusd_contract(web3, CUSTODIAN_FILE_PATH, "Custodian", [signer1,signer2], _defaultTimeLock, _extendedTimeLock, _primary)
    # print("Custodian1   : "+Custodian1.address)
    #
    # #第二步，部署Custodian 合约实例 2
    # _defaultTimeLock=172800
    # _extendedTimeLock = 604800
    # Custodian2 = deploy_gusd_contract(web3, CUSTODIAN_FILE_PATH, "Custodian", [signer1,signer2], _defaultTimeLock, _extendedTimeLock, _primary)
    # print("Custodian2   : "+Custodian2.address)
    #
    # #第三步，部署未据名合约实例 1
    # #等待实现
    # deployContract = deploy_gusd_contract(web3, DEPLOY_FILE_PATH, 'deploy')
    # print("deployContract:"+deployContract.address)
    #
    # #第四步，部署ERC20Store 合约实例
    # # ERC20Store=deploy_gusd_contract(web3,ERC20STORE_FILE_PATH,deployContract)
    # ERC20Store = deploy_gusd_contract(web3, ERC20STORE_FILE_PATH, 'ERC20Store', deployContract.address)
    # print("ERC20Store   : " + ERC20Store.address)
    #
    # #第五步，部署 ERC20Proxy 合约实例
    # ERC20Proxy=deploy_gusd_contract(web3, ERC20PROXY_FILE_PATH, 'ERC20Proxy',"Gemini dollar","GUSD",2, deployContract.address)
    # print("ERC20Proxy   : " + ERC20Proxy.address)
    #
    # #第六步，部署 ERC20Impl 合约实例
    # ERC20Impl=deploy_gusd_contract(web3, ERC20IMPL_FILE_PATH, 'ERC20Impl', ERC20Proxy.address, ERC20Store.address, deployContract.address, _sweeper)
    # print("ERC20Impl    : " + ERC20Impl.address)
    #
    # #第七步，部署PrintLimiter 合约实例
    # PrintLimiter=deploy_gusd_contract(web3, PRINTLIMITER_FILE_PATH, 'PrintLimiter', ERC20Impl.address, Custodian1.address, _sweeper, 10000000000)
    # print("PrintLimiter : " + PrintLimiter.address)



    #第八步，通过未据名合约实例 1
    #修改 ERC20Impl 合约上的 custodian
    #修改 ERC20Impl 合约上的 custodian
    #修改 ERC20Proxy 合约上的 custodian
    #修改 ERC20Store 合约上的 custodian
    #修改 ERC20Proxy 合约上的 erc20Impl
    #修改 ERC20Store 合约上的 erc20Impl
    # deployContract.functions.initialize(ERC20Store.address, ERC20Proxy.address, ERC20Impl.address, Custodian2.address, PrintLimiter.address).transact()

    #
    # Custodian1   : 0x1087aB99F519798A2c7F2CEF6a42f9274F64D641
    # Custodian2   : 0xe0526B779D6F326a28156809e24c894AE455CbBD
    # deployContract:0x16D1F0F617ec517f223476c813dE567A015857EC
    # ERC20Store   : 0x4c8538fAB25417B225e03441b52736Ff9Ed65295
    # ERC20Proxy   : 0x12E8F1F738E5E6124A2883A0f55d48bA6A355e82
    # ERC20Impl    : 0x5Fd0B7Ab187773cCbAe3FA87a14B13745A602165
    # PrintLimiter : 0x4f4399DDe7687794B141254A34Dd862891ACa1B6


    web3=connectCanacheHTTPWeb3("http://127.0.0.1:8545")
    print(web3.eth.accounts)
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    deployContract = get_gusd_contract(web3, DEPLOY_FILE_PATH,'deploy','0x16D1F0F617ec517f223476c813dE567A015857EC')
    # deployContract.functions.initialize(ERC20Store.address, ERC20Proxy.address, ERC20Impl.address, Custodian2.address,
    #                                     PrintLimiter.address).transact()
    deployContract.functions.initialize('0x4c8538fAB25417B225e03441b52736Ff9Ed65295',
                                        '0x12E8F1F738E5E6124A2883A0f55d48bA6A355e82',
                                        '0x5Fd0B7Ab187773cCbAe3FA87a14B13745A602165',
                                        '0xe0526B779D6F326a28156809e24c894AE455CbBD',
                                        '0x4f4399DDe7687794B141254A34Dd862891ACa1B6').transact()


