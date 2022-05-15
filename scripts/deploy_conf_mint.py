#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, network, config
from scripts.helpful_scripts import get_publish_source
from scripts.mint_oneTM_nft import mint2
from web3 import Web3

setPrice = config["networks"][network.show_active()]["token_price"]
metadataLibrary = config["networks"][network.show_active()]["metadata_library"]
collectionVault = config["networks"][network.show_active()]["collection_vault"]


isActive = True


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
    one_tm_show_off = OneTMShowOff.deploy(
        setPrice,
        {"from": dev},
        publish_source=get_publish_source(),
    )
    # make sure you've got the latest contract
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]

    one_tm_show_off.setGallery(metadataLibrary, {"from": dev})
    one_tm_show_off.setVault(collectionVault, {"from": dev})
    one_tm_show_off.setActive(isActive, {"from": dev})

    deploy10()

    return one_tm_show_off
