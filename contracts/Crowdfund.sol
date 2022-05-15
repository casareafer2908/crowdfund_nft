// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";
import "./ERC721Enumerable.sol";

abstract contract Crowdfunds is Context, Ownable, ERC721Enumerable {
    // ETH_RAISED,  ==> 1
    // MINT_NUMBER, ==> 2
    // DEFAULT      ==> 0

    enum Crowdfund_Method {
        ETH_RAISED,
        MINT_NUMBER,
        DEFAULT
    }
    Crowdfund_Method internal crowdfund_method;
    uint256 goal;
    bool goalMet;

    constructor() {
        crowdfund_method = Crowdfund_Method.DEFAULT;
        goal = 0;
        goalMet = false;
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

    function _setCrowdfundGoal(uint256 _goal) internal onlyOwner {
        require(
            crowdfund_method != Crowdfund_Method.DEFAULT,
            "Crowdfund Method is not set"
        );
        goal = _goal;
    }

    function _verifyCrowdfundGoal() internal returns (bool) {
        // ETH Raised goal
        if (crowdfund_method = Crowdfund_Method.ETH_RAISED) {
            if (address(this).balance >= goal) {
                return true;
            } else {
                return false;
            }
        }
        // Number of mints goal
        else {
            if (totalSupply() >= goal) {
                return true;
            } else {
                return false;
            }
        }
    }

    function _setCrowdfundSalePeriod() internal onlyOwner {}
}
