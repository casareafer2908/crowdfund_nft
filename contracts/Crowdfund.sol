// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";

abstract contract Crowdfunds is Context, Ownable {
    // ETH_RAISED,  ==> 1
    // MINT_NUMBER, ==> 2
    // DEFAULT      ==> 0

    enum Crowdfund_Method {
        ETH_RAISED,
        MINT_NUMBER,
        DEFAULT
    }
    Crowdfund_Method internal crowdfund_method;

    constructor() {
        crowdfund_method = Crowdfund_Method.DEFAULT;
    }

    function _setCrowdfundMethod(uint256 method) internal onlyOwner {
        require(method <= 2, "Invalid Crowdfund Method");
        require(method >= 0, "Invalid Crowdfund Method");
        if (method == 0) {
            crowdfund_method = Crowdfund_Method.DEFAULT;
        } else if (method == 1) {
            crowdfund_method = Crowdfund_Method.ETH_RAISED;
        } else {
            crowdfund_method = Crowdfund_Method.MINT_NUMBER;
        }
    }

    function readCrowdfundMethod() public view returns (bytes32) {
        bytes32 method;
        if (crowdfund_method == Crowdfund_Method.DEFAULT) {
            method = "Default";
        } else if (crowdfund_method = Crowdfund_Method.ETH_RAISED) {
            method = "ETH Raised";
        } else {
            method = "Mints number";
        }
        return method;
    }

    function _setCrowdfundGoal(uint256 goal) internal onlyOwner {}

    function _setCrowdfundSalePeriod() internal onlyOwner {}

    function _verifyCrowdfundGoal() internal onlyOwner returns (bool) {}
}
