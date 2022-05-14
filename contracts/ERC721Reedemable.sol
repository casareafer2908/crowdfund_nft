// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

abstract contract ERC721Reedemable is Context, Ownable, ERC721 {
    bool public redeemable = false;
    uint256 _redeemsLimit;
    uint256 _tokenRemainingRedeems;
    enum Redeem_State {
        ACTIVE,
        PROCESSING,
        CLOSED
    }

    //maps

    mapping(uint256 => Redeem_State) public tokenIdToRedeemState;
    mapping(uint256 => uint256) public tokenIdToRemainingRedeems;
    event RequestedRedeem(bytes32 indexed requestId);

    function setTokenRedeems(uint256 tokenId, uint256 redeemsLimit)
        public
        onlyOwner
    {}

    function redeem(address tokenId) public {
        require(
            _isApprovedOrOwner(msg.sender, tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        require(tokenIdToRedeemState[tokenId] == Redeem_State.ACTIVE);
    }
}
