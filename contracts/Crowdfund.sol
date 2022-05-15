// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";

abstract contract Crowdfund is Context, Ownable {
    enum Crowdfund_Method {
        ETH_RAISED,
        MINT_NUMBER,
        DEFAULT
    }
    Crowdfund_Method internal crowdfund_method;
    uint256 goal;
    bool goalMet;
    uint256 startDate;
    uint256 endDate;

    constructor() {
        crowdfund_method = Crowdfund_Method.DEFAULT;
        goal = 0;
        goalMet = false;
        startDate = 1;
        endDate = 1;
    }

    function _setCrowdfundMethod(uint256 method) internal onlyOwner {
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
        } else if (crowdfund_method == Crowdfund_Method.ETH_RAISED) {
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

    function readCrowdfundGoal() external returns (uint256) {
        return goal;
    }

    function _verifyCrowdfundGoal(uint256 supply) internal returns (bool) {
        //TODO: Add Safe Withdraw Logic. If the owner withdraws funds from the contract,
        //the goal trigger will not be met, therefore redeems will be closed on the next mint

        // ETH Raised goal
        if (crowdfund_method == Crowdfund_Method.ETH_RAISED) {
            //checks if the contract address reached the goal
            if (address(this).balance >= goal) {
                return true;
            } else {
                return false;
            }
        }
        // Number of mints goal
        else {
            if (supply >= goal) {
                return true;
            } else {
                return false;
            }
        }
    }

    function _setSalePeriod(uint256 _startDate, uint256 _endDate)
        internal
        onlyOwner
    {
        startDate = _startDate;
        endDate = _endDate;
    }

    function _verifySalePeriod(uint256 txTime)
        internal
        onlyOwner
        returns (bool)
    {
        if (startDate == 0 && endDate == 0) {
            return true;
        } else if (txTime >= startDate && txTime < endDate) {
            return true;
        } else {
            return false;
        }
    }
}
