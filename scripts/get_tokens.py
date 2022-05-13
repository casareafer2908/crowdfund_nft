#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print("Working on " + network.show_active())
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]
    ammountOfNfts = one_tm_show_off.totalSupply()
    print(f"Total NFTs Minted ==> {ammountOfNfts}")
