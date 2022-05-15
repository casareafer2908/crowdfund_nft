// SPDX-License-Identifier: MIT

// Show off contract to get a job at 1TMShow

pragma solidity ^0.8.7;

import "./ERC721Enumerable.sol";
import "./ERC721Reedemable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract OneTMShowOff is ERC721Enumerable, Ownable, ERC721Reedemable {
    using Strings for uint256;

    address public vault; // Contract to recieve ETH raised in sales
    bool public isActive; // Control for public sale
    string public gallery; // Reference to image and metadata storage
    uint256 public price; // Amount of ETH required per mint

    // Sets `price` upon deployment
    constructor(uint256 _price) ERC721("OneTMShowOff", "OneTM") {
        setPrice(_price);
    }

    ////////////////////////////////
    ////////////////////////////////////////////
    ///////////UNDER CONSTRUCTION//////////////////////
    ///////////////////////////////////////////
    ////////////////////////////////

    //Sets number of redeems limit to a single token
    function setTokenRedeems(uint256 _tokenId, uint256 _redeemsLimit)
        public
        onlyOwner
    {
        require(_exists(_tokenId), "ERC721 Token doesn't exist");
        _setTokenRedeems(_tokenId, _redeemsLimit);
    }

    //Sets number of redeems to all minted tokens
    function setAllTokensRedeems(uint256 _redeemsLimit) public onlyOwner {
        uint256 _supply = totalSupply();
        require(_supply > 0, "No tokens minted to set redeem limit");
        _setAllTokensRedeems(_redeemsLimit, _supply);
    }

    // Reads available redeems for a token
    function readTokenRedeemLimit(uint256 _tokenId)
        public
        view
        returns (uint256)
    {
        require(_exists(_tokenId), "ERC721 Token doesn't exist");
        return _readTokenRedeemLimit(_tokenId);
    }

    // Set redeems Available - Unavailable
    function setRedeemState(bool _state) public onlyOwner {
        _setRedeemState(_state);
    }

    //TODO implement function
    function redeem(uint256 _tokenId, uint256 _ammount) public {
        _redeem(_tokenId, _ammount);
    }

    //TODO update a single token metadata
    function updateTokenMetadata(bytes32 _metadata, uint256 _tokenId) public {}

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

    // Minting function used in the public sale
    function mint(uint256 _amount) external payable {
        uint256 supply = totalSupply();

        require(isActive, "Not Active");
        require(_amount < 3, "Amount Denied");
        require(supply + _amount < 556, "Supply Denied");
        require(tx.origin == msg.sender, "Contract Denied");
        require(msg.value >= price * _amount, "Ether Amount Denied");

        for (uint256 i; i < _amount; i++) {
            _safeMint(msg.sender, supply + i);
        }
    }

    // Send balance of contract to address referenced in `vault`
    function withdraw() external payable onlyOwner {
        require(vault != address(0), "Vault Invalid");
        require(payable(vault).send(address(this).balance));
    }
}
