import pytest


@pytest.mark.parametrize(
    "num1",
    "num2",
    "result",
    [
        (1, 2, 3),
        (3, 4, 7),
        (2, 2, 4),
        (1, 2, 3),
        (1, 2, 3),
        (1, 2, 3),
        (1, 2, 3),
        (1, 2, 3),
    ],
)
def test_add(num1, num2, result):
    assert (num1 + num2) == result


def can_configure_project():
    # Act
    print(f"Set Vault ==> {collectionVault}")
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

    assert one_tm_show_off.vault({"from": dev}) == collectionVault
