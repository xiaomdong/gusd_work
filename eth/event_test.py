import eth_interface

if __name__ == '__main__':
    web3=eth_interface.connectHTTPWeb3("http://127.0.0.1:8545")
    # step1()
    contract_= eth_interface.step2(web3)
    event_filter=contract_.events.Instructor.createFilter(fromBlock='latest')
    eth_interface.main(event_filter)