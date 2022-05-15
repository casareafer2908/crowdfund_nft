#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, network, config
from scripts.helpful_scripts import get_publish_source
from scripts.mint_oneTM_nft import mint2
from web3 import Web3

setPrice = config["networks"][network.show_active()]["token_price"]
metadataLibrary = config["networks"][network.show_active()]["metadata_library"]
collectionVault = config["networks"][network.show_active()]["collection_vault"]


isActive = True
redeemsLimit = 1
setSupply = 555
mintsPerWallet = 10

# Crowdfund method
# 0 => Default
# 1 => Eth Raised
# 2 => Mint number
crowfundMethod = 2
crowdfundGoal = 3


def deploy10():
    toDeploy = 1
    for n in range(toDeploy):
        print(f"run number {(n + 1)}")
        mint2()


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # human readable plz
    print(f"Set token price ==> {Web3.fromWei(setPrice, 'ether')} ETH")
    print(f"Set Supply Limit ==> {setSupply}")
    print(f"Set redeems per NFT ==> {redeemsLimit}")
    one_tm_show_off = OneTMShowOff.deploy(
        setPrice,
        setSupply,
        {"from": dev},
        publish_source=get_publish_source(),
    )
    # make sure you've got the latest contract
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]
    one_tm_show_off.setGallery(metadataLibrary, {"from": dev})
    one_tm_show_off.setVault(collectionVault, {"from": dev})
    one_tm_show_off.setTokenRedeemsLimit(redeemsLimit, {"from": dev})
    one_tm_show_off.setCrowdfundMethod(crowfundMethod, {"from": dev})
    one_tm_show_off.setCrowdfundGoal(crowdfundGoal, {"from": dev})
    one_tm_show_off.setMintablePerWallet(mintsPerWallet, {"from": dev})
    one_tm_show_off.setMintActive(isActive, {"from": dev})
    deploy10()

    return one_tm_show_off
