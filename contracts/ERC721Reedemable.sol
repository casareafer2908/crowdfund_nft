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

    constructor() public {
        redeem_state = Redeem_State.OFF;
    }

    //maps
    mapping(uint256 => Redeem_State) public tokenIdToRedeemState;
    mapping(uint256 => uint256) public tokenIdToRemainingRedeems;

    //Sets number of redeems limit to a single token
    function _setTokenRedeems(uint256 tokenId, uint256 redeemsLimit)
        internal
        onlyOwner
    {
        tokenIdToRemainingRedeems[tokenId] = redeemsLimit;
    }

    //Sets number of redeems limit to minted tokens
    function _setAllTokensRedeems(uint256 redeemsLimit, uint256 tokenList)
        internal
        onlyOwner
    {
        while (i < tokenList) {
            tokenIdToRemainingRedeems[i] = redeemsLimit;
            i++;
        }
    }

    //Returns available redeems
    function _readTokenRedeemLimit(uint256 tokenId)
        internal
        view
        returns (uint256)
    {
        return tokenIdToRemainingRedeems[tokenId];
    }

    function readRedeemState() public view returns (bytes32) {
        return redeem_state;
    }

    //internal since it can only be opened when the goal is met
    function _setRedeemState(uint256 state) internal onlyOwner {
        redeem_state = state;
    }

    function redeem(address tokenId) public {
        require(
            _isApprovedOrOwner(msg.sender, tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        require(tokenIdToRedeemState[tokenId] == Redeem_State.ON);
    }
}
