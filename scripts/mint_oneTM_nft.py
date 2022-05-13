#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, config
from web3 import Web3

# mint tokens
mintAmmount = 2
payable = mintAmmount * 0.01


def mint2():
    dev = accounts.add(config["wallets"]["from_key"])

    # Get the latest deployed contract
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]
    print(f"{mintAmmount} tokens for {payable} ether")
    one_tm_show_off.mint(
        mintAmmount, {"from": dev, "value": Web3.toWei(payable, "ether")}
    )
