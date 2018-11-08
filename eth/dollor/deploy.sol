pragma solidity ^0.4.21;

import "./ERC20Impl.sol";
import "./ERC20Proxy.sol";
import "./ERC20Store.sol";

contract deploy {
//    function deploy(){
//
//    }
////
////    function initialize(address _owner, address _output, address _fundingAddress, address _milestoneAddress, address _proposalsAddress){
////
////    }

    function initialize(address _ERC20Store, address _ERC20Proxy, address _ERC20Impl, address _Custodian2, address _PrintLimiter) public{
	    ERC20Store(_ERC20Store).confirmImplChange(ERC20Store(_ERC20Store).requestImplChange(_ERC20Impl));
        ERC20Proxy(_ERC20Proxy).confirmImplChange(ERC20Proxy(_ERC20Proxy).requestImplChange(_ERC20Impl));
        ERC20Store(_ERC20Store).confirmCustodianChange(ERC20Store(_ERC20Store).requestCustodianChange(_PrintLimiter));
        ERC20Proxy(_ERC20Proxy).confirmCustodianChange(ERC20Proxy(_ERC20Proxy).requestCustodianChange(_PrintLimiter));
        ERC20Impl(_ERC20Impl).confirmCustodianChange(ERC20Impl(_ERC20Impl).requestCustodianChange(_PrintLimiter));
    }
}
