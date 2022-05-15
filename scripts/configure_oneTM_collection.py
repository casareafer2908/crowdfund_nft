#!/usr/bin/python3
from brownie import OneTMShowOff, accounts, network, config
import datetime
import pytz

metadataLibrary = config["networks"][network.show_active()]["metadata_library"]
collectionVault = config["networks"][network.show_active()]["collection_vault"]

# bool to control mint
isActive = True
startTime = datetime.datetime(
    2022, 5, 15, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
)
endTime = datetime.datetime(
    2022, 5, 17, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
)

testTime = datetime.datetime(
    2022, 5, 16, 6, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
)


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())

    # Get the latest deployed contract
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]
    one_tm_show_off.setSalePeriod(
        startTime.timestamp(), endTime.timestamp(), {"from": dev}
    )
    # one_tm_show_off.setGallery(metadataLibrary, {"from": dev})
    # one_tm_show_off.setVault(collectionVault, {"from": dev})
    # one_tm_show_off.setMintActive(isActive, {"from": dev})

    return one_tm_show_off
