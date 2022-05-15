// SPDX-License-Identifier: MIT

// Show off contract to get a job at 1TMShow

pragma solidity ^0.8.7;

import "./ERC721Enumerable.sol";
import "./ERC721Reedemable.sol";
import "./Crowdfund.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract OneTMShowOff is
    ERC721Enumerable,
    Ownable,
    ERC721Reedemable,
    Crowdfund
{
    using Strings for uint256;

    address public vault; // Contract to recieve ETH raised in sales
    bool public isActive; // Control for public sale
    string public gallery; // Reference to image and metadata storage
    uint256 public price;
    uint256 public supplyLimit; // Amount of ETH required per mint
    uint256 public mintablePerWallet;
    uint256 internal redeemsLimit;

    // Sets `price`, `nft supply`, `mints per wallet` and `redeems per nft` upon deployment
    constructor(uint256 _price, uint256 _supplyLimit)
        ERC721("OneTMShowOff", "OneTM")
    {
        setPrice(_price);
        setSupply(_supplyLimit);
        mintablePerWallet = 2;
        redeemsLimit = 0;
    }

    ////////////////////////////////
    ////////////////////////////////////////////
    ///////////UNDER CONSTRUCTION//////////////////////
    ///////////////////////////////////////////
    ////////////////////////////////

    //sets the collection supply limit
    function setSupply(uint256 _supplyLimit) public onlyOwner {
        supplyLimit = _supplyLimit;
    }

    // Sets number of redeems for newly minted tokens
    function setTokenRedeemsLimit(uint256 _number) external onlyOwner {
        redeemsLimit = _number;
    }

    // Sets number of redeems limit to a single token
    function setTokenRedeems(uint256 tokenId, uint256 redeemsLimit) internal {
        _setTokenRedeems(tokenId, redeemsLimit);
    }

    //Override the number of redeems to all minted tokens
    function setAllTokensRedeems(uint256 _redeemsLimit) external onlyOwner {
        uint256 supply = totalSupply();
        require(supply > 0, "No tokens minted to set redeem limit");
        _setAllTokensRedeems(_redeemsLimit, supply);
    }

    // Reads available redeems for a token
    function readTokenRedeemLimit(uint256 tokenId)
        external
        view
        returns (uint256)
    {
        require(_exists(tokenId), "ERC721 Token doesn't exist");
        return _readTokenRedeemLimit(tokenId);
    }

    // Redeem control
    function setRedeemState(bool state) internal {
        _setRedeemState(state);
    }

    // Crowdfund Methods:
    // DEFAULT      ==> 0
    // ETH_RAISED,  ==> 1
    // MINT_NUMBER, ==> 2
    function setCrowdfundMethod(uint256 _method) external onlyOwner {
        require(_method <= 2, "Invalid Crowdfund Method");
        require(_method >= 0, "Invalid Crowdfund Method");
        _setCrowdfundMethod(_method);
    }

    function setCrowdfundGoal(uint256 _goal) external onlyOwner {
        _setCrowdfundGoal(_goal);
    }

    function redeem(uint256 tokenId, uint256 ammount) external {
        require(
            ownerOf(tokenId) == msg.sender,
            "You are not the owner this token"
        );
        _redeem(tokenId, ammount);
    }

    //TODO update a single token metadata after redeem
    function updateTokenMetadata(bytes32 metadata, uint256 tokenId) public {}

    ////////////////////////////////
    ////////////////////////////////////////////
    ///////////UNDER CONSTRUCTION//////////////////////
    ///////////////////////////////////////////
    ////////////////////////////////

    // Override of `_baseURI()` that returns `gallery`
    function _baseURI() internal view virtual override returns (string memory) {
        return gallery;
    }

    // Sets `isActive` to turn on/off minting in `mint()`
    function setMintActive(bool _isActive) external onlyOwner {
        isActive = _isActive;
    }

    // Sets `gallery` to be returned by `_baseURI()`
    function setGallery(string calldata _gallery) external onlyOwner {
        gallery = _gallery;
    }

    // Sets `price` to be used in `presale()` and `mint()`(called on deployment)
    function setPrice(uint256 _price) public onlyOwner {
        price = _price;
    }

    // Sets `vault` to recieve ETH from sales and used within `withdraw()`
    function setVault(address _vault) external onlyOwner {
        vault = _vault;
    }

    // Sets `max mints per wallet`
    function setMintablePerWallet(uint256 _number) external onlyOwner {
        mintablePerWallet = _number;
    }

    // Minting function used in the public sale
    function mint(uint256 _amount) external payable {
        uint256 supply = totalSupply();

        require(isActive, "Not Active");
        require(_amount <= mintablePerWallet, "Amount Denied");
        require(supply + _amount <= supplyLimit, "Supply Denied");
        require(tx.origin == msg.sender, "Contract Denied");
        require(msg.value >= price * _amount, "Ether Amount Denied");

        for (uint256 i; i < _amount; i++) {
            _safeMint(msg.sender, supply + i);
            setTokenRedeems(supply + i, redeemsLimit);
        }
        //If the goal is met, holders will be able to redeem
        if (_verifyCrowdfundGoal(totalSupply())) {
            setRedeemState(true);
        }
    }

    // Send balance of contract to address referenced in `vault`
    function withdraw() external payable onlyOwner {
        require(vault != address(0), "Vault Invalid");
        require(payable(vault).send(address(this).balance));
    }
}
