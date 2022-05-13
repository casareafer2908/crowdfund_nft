#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, network, config
from scripts.helpful_scripts import get_publish_source
from web3 import Web3

setPrice = config["networks"][network.show_active()]["token_price"]


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
    return one_tm_show_off
