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
    mapping(uint256 => uint256) internal tokenIdToRemainingRedeems;

    //events
    event SetTokenLimit(uint256 tokenId, uint256 redeemsLimit);
    event SetAllTokensLimit(uint256 redeemsLimit);
    event redeemGoods(uint256 redeemAmount, uint256 redeemLeft);

    //Sets number of redeems limit to a single token
    function _setTokenRedeems(uint256 _tokenId, uint256 _redeemsLimit)
        internal
        onlyOwner
    {
        tokenIdToRemainingRedeems[_tokenId] = _redeemsLimit;
        emit SetTokenLimit(_tokenId, _redeemsLimit);
    }

    //Sets number of redeems limit to minted tokens
    function _setAllTokensRedeems(uint256 _redeemsLimit, uint256 _tokenList)
        internal
        onlyOwner
    {
        uint256 i = 0;
        while (i < _tokenList) {
            tokenIdToRemainingRedeems[i] = _redeemsLimit;
            i++;
        }
        emit SetAllTokensLimit(_redeemsLimit);
    }

    //Returns available redeems
    function _readTokenRedeemLimit(uint256 _tokenId)
        internal
        view
        returns (uint256)
    {
        return tokenIdToRemainingRedeems[_tokenId];
    }

    function readRedeemState() public view returns (bool) {
        bool active = (redeem_state == Redeem_State.ON ? true : false);
        return active;
    }

    //internal since it can only be opened when the goal is met
    function _setRedeemState(bool _state) internal onlyOwner {
        redeem_state = (_state == true ? Redeem_State.ON : Redeem_State.OFF);
    }

    //TODO save redeem times, update token metadata
    function _redeem(uint256 _tokenId, uint256 _ammount) internal {
        require(
            redeem_state == Redeem_State.ON,
            "Redeems are not available right now"
        );
        require(
            tokenIdToRemainingRedeems[_tokenId] > 0,
            "You've not redeems left"
        );
        require(
            tokenIdToRemainingRedeems[_tokenId] > _ammount,
            "You've not enough redeems"
        );
        tokenIdToRemainingRedeems[_tokenId] =
            tokenIdToRemainingRedeems[_tokenId] -
            1;
        emit redeemGoods(_ammount, tokenIdToRemainingRedeems[_tokenId]);
    }
}
