// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Enumerable.sol";
import "./ERC721.sol";

abstract contract ERC721Reedemable is Context, Ownable {
    //states:
    //0 -> OFF - People can't redeem
    //1 -> ON - People can redeem
    enum Redeem_State {
        OFF,
        ON
    }
    Redeem_State public redeem_state;

    constructor() {
        redeem_state = Redeem_State.OFF;
    }

    //maps
    //todo do this map internal
    mapping(uint256 => Redeem_State) public tokenIdToRedeemState;
    mapping(uint256 => uint256) internal tokenIdToRemainingRedeems;

    //events
    event SetTokenLimit(uint256 tokenId, uint256 redeemsLimit);
    event SetAllTokensLimit(uint256 redeemsLimit);

    //Sets number of redeems limit to a single token
    function _setTokenRedeemss(uint256 tokenId, uint256 redeemsLimit)
        internal
        onlyOwner
    {
        tokenIdToRemainingRedeems[tokenId] = redeemsLimit;
        emit SetTokenLimit(tokenId, redeemsLimit);
    }

    //Sets number of redeems limit to minted tokens
    function _setAllTokensRedeemss(uint256 redeemsLimit, uint256 tokenList)
        internal
        onlyOwner
    {
        uint256 i = 0;
        while (i < tokenList) {
            tokenIdToRemainingRedeems[i] = redeemsLimit;
            i++;
        }
        emit SetAllTokensLimit(redeemsLimit);
    }

    //Returns available redeems
    function _readTokenRedeemLimit(uint256 tokenId)
        internal
        view
        returns (uint256)
    {
        return tokenIdToRemainingRedeems[tokenId];
    }

    function readRedeemState() public view returns (bool) {
        bool active = (redeem_state == Redeem_State.ON ? true : false);
        return active;
    }

    //internal since it can only be opened when the goal is met
    function _setRedeemState(bool state) internal onlyOwner {
        redeem_state = (state == true ? Redeem_State.ON : Redeem_State.OFF);
    }

    //TODO save redeem times, update token metadata
    function redeem(uint256 tokenId) public {
        require(tokenIdToRedeemState[tokenId] == Redeem_State.ON);
    }
}
