// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";

abstract contract ERC721Reedemable is Context, Ownable {
    //states:
    //0 -> OFF - People can't redeem
    //1 -> ON - People can redeem
    enum Redeem_State {
        OFF,
        ON
    }
    Redeem_State internal redeem_state;

    constructor() {
        redeem_state = Redeem_State.OFF;
    }

    //maps
    mapping(uint256 => uint256) public tokenIdToRemainingRedeems;

    //events
    event SetTokenLimit(uint256 tokenId, uint256 redeemsLimit);
    event SetAllTokensLimit(uint256 redeemsLimit);
    event redeemGoods(uint256 redeemAmount, uint256 redeemLeft);

    //Sets number of redeems limit to a single token
    function _setTokenRedeems(uint256 tokenId, uint256 redeemsLimit)
        internal
        onlyOwner
    {
        tokenIdToRemainingRedeems[tokenId] = redeemsLimit;
        emit SetTokenLimit(tokenId, redeemsLimit);
    }

    //Sets number of redeems limit to minted tokens
    function _setAllTokensRedeems(uint256 redeemsLimit, uint256 tokenList)
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

    function _redeem(uint256 tokenId, uint256 ammount) internal {
        require(
            redeem_state == Redeem_State.ON,
            "Redeems are not available right now"
        );
        uint256 availableRedeems = tokenIdToRemainingRedeems[tokenId];
        require(availableRedeems > 0, "You have no redeems left");
        require(availableRedeems > ammount, "You have not enough redeems");
        tokenIdToRemainingRedeems[tokenId] = availableRedeems - 1;
        emit redeemGoods(ammount, tokenIdToRemainingRedeems[tokenId]);
    }
}
