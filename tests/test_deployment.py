import time
import pytest
from brownie import OneTMShowOff, accounts, network, config
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_publish_source,
)
from scripts.mint_oneTM_nft import mint2
from web3 import Web3


def test_can_create_OneTMShowOff_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    print("Arrange tests")
    print(network.show_active())
    dev = accounts.add(config["wallets"]["from_key"])
    setPrice = config["networks"][network.show_active()]["token_price"]
    metadataLibrary = config["networks"][network.show_active()]["metadata_library"]
    collectionVault = config["networks"][network.show_active()]["collection_vault"]
    isActive = True
    redeemsLimit = 1
    setSupply = 555
    mintsPerWallet = 10
    mintAmmount = 1
    payable = mintAmmount * 0.01

    # Crowdfund method
    # 0 => Default
    # 1 => Eth Raised
    # 2 => Mint number
    crowfundMethod = 2
    crowdfundGoal = 3

    print(f"Set token price ==> {Web3.fromWei(setPrice, 'ether')} ETH")
    print(f"Set Supply Limit ==> {setSupply}")
    print(f"Set Vault ==> {collectionVault}")
    print("Deploying contract...")
    one_tm_show_off = OneTMShowOff.deploy(
        setPrice,
        setSupply,
        {"from": dev},
        publish_source=get_publish_source(),
    )
    # Act
    print("Contract deployed, setting Gallery...")
    one_tm_show_off.setGallery(metadataLibrary, {"from": dev})
    print("Gallery set, setting Vault...")
    one_tm_show_off.setVault(collectionVault, {"from": dev})
    print("Vault set, setting Token Redeems Limit...")
    one_tm_show_off.setTokenRedeemsLimit(redeemsLimit, {"from": dev})
    print("Token Redeems Limit set, setting Crowdfund Method...")
    one_tm_show_off.setCrowdfundMethod(crowfundMethod, {"from": dev})
    print("Crowdfund method set, setting Crowdfund Goal...")
    one_tm_show_off.setCrowdfundGoal(crowdfundGoal, {"from": dev})
    print("Crowdfund Goal set, setting Mints per transaction...")
    one_tm_show_off.setMintablePerWallet(mintsPerWallet, {"from": dev})
    print("Mints per transaction set, setting Mint Active...")
    one_tm_show_off.setMintActive(isActive, {"from": dev})
    print(f"Mint active, minting {mintAmmount} token for {payable} ether")
    one_tm_show_off.mint(
        mintAmmount, {"from": dev, "value": Web3.toWei(payable, "ether")}
    )
    print("wait 5 secs for blockchain to update")
    time.sleep(5)

    # Assert
    assert one_tm_show_off.totalSupply({"from": dev}) == mintAmmount
    assert one_tm_show_off.supplyLimit({"from": dev}) == setSupply
    assert one_tm_show_off.price({"from": dev}) == setPrice
    assert one_tm_show_off.vault({"from": dev}) == collectionVault
