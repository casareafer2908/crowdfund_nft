#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, network, config

metadataLibrary = config["networks"][network.show_active()]["metadata_library"]
collectionVault = config["networks"][network.show_active()]["collection_vault"]

# bool to control mint
isActive = True


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())

    # Get the latest deployed contract
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]

    one_tm_show_off.setGallery(metadataLibrary, {"from": dev})
    one_tm_show_off.setVault(collectionVault, {"from": dev})
    one_tm_show_off.setActive(isActive, {"from": dev})

    return one_tm_show_off
