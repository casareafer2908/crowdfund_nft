import brownie
import pytest
from datetime import datetime
import pytz
import time
from brownie import OneTMShowOff, accounts, network, config, exceptions
from scripts.helpful_scripts import (
    get_publish_source,
)
from web3 import Web3


@pytest.fixture
def developer():
    return accounts.add(config["wallets"]["from_key"])


@pytest.fixture
def badActor():
    return accounts.add(config["wallets"]["from_key_test"])


@pytest.fixture
def setPrice():
    return config["networks"][network.show_active()]["token_price"]


@pytest.fixture
def setSupply():
    return 555


@pytest.fixture
def metadataLibrary():
    return config["networks"][network.show_active()]["metadata_library"]


@pytest.fixture
def collectionVault():
    return config["networks"][network.show_active()]["collection_vault"]


@pytest.fixture
def failTestTimeNotYetStart():
    startTime = datetime(2022, 6, 17, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    endTime = datetime(2022, 7, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    return [startTime.timestamp(), endTime.timestamp()]


@pytest.fixture
def failTestTimeEnded():
    startTime = datetime(2022, 2, 17, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    endTime = datetime(2022, 4, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    return [startTime.timestamp(), endTime.timestamp()]


@pytest.fixture
def succeedTestTime():
    startTime = datetime(2022, 5, 17, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    endTime = datetime(2022, 7, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    return [startTime.timestamp(), endTime.timestamp()]


@pytest.fixture
def succeedTestTimeAlwaysOpen():
    startTime = 0
    endTime = 0
    return [startTime, endTime]


@pytest.fixture
def alwaysActiveTestTime():
    startTime = 0
    endTime = 0
    return [startTime, endTime]


@pytest.fixture
def mintsPerTransaction():
    return 4


@pytest.fixture
def redeemsLimitPerToken():
    return 1


# Deploy a contract
@pytest.fixture
def rinkeby_test_contract(setPrice, developer, setSupply):
    print("Deploying test contract...")
    deployed = OneTMShowOff.deploy(
        setPrice,
        setSupply,
        {
            "from": developer,
        },
        publish_source=get_publish_source(),
    )
    print(f"Contract deployed in address ==> {deployed.address}")
    return deployed


# Get the latest deployed contract
@pytest.fixture
def latest_contract(OneTMShowOff):
    contract = OneTMShowOff[len(OneTMShowOff) - 1]
    print(f"Used Contract address ==> {contract.address}")
    return contract


@pytest.fixture
def gas_failed_tx():
    return 500000


###
# Test Contract Deployment
###

# Test that the contract deploys successfully
def test_contract_deployment(rinkeby_test_contract, setPrice, setSupply, developer):
    print(f"Assert that the price set is correct...")
    assert rinkeby_test_contract.price({"from": developer}) == setPrice
    print(f"Assert that the supply limit is correct...")
    assert rinkeby_test_contract.supplyLimit({"from": developer}) == setSupply
    print("Done!")


# Test that the contract cant be configured by Bad Actors
def test_contract_configuration(
    latest_contract,
    developer,
    redeemsLimitPerToken,
    metadataLibrary,
    mintsPerTransaction,
    collectionVault,
):
    print("Setting Gallery...")
    latest_contract.setGallery(metadataLibrary, {"from": developer})
    print("Gallery set, setting Vault...")
    latest_contract.setVault(collectionVault, {"from": developer})
    print("Vault set, setting Token Redeems Limit...")
    latest_contract.setTokenRedeemsLimit(redeemsLimitPerToken, {"from": developer})
    print("Token Redeems Limit set, setting Mints per transaction...")
    latest_contract.setMintablePerTransaction(mintsPerTransaction, {"from": developer})
    print("Mints per transaction set, setting mint -->OFF<--")
    latest_contract.setMintActive(False, {"from": developer})
    print("Mint set -->OFF<-- , Setting max mints per transaction")
    print("Set max mints per transaction")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Asserting all configurations...")

    assert latest_contract.gallery({"from": developer}) == metadataLibrary
    assert latest_contract.vault({"from": developer}) == collectionVault
    assert latest_contract.redeemsLimit({"from": developer}) == redeemsLimitPerToken
    assert (
        latest_contract.mintablePerTransaction({"from": developer})
        == mintsPerTransaction
    )
    assert latest_contract.isActive({"from": developer}) == False


# Test that a bad actor can't change configurations
def test_contract_configuration_bad_actor(
    latest_contract,
    badActor,
    redeemsLimitPerToken,
    metadataLibrary,
    mintsPerTransaction,
    collectionVault,
    gas_failed_tx,
):
    print("Setting Gallery...")
    with pytest.raises(ValueError):
        latest_contract.setGallery(
            metadataLibrary,
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            },
        )
    print("Gallery NOT SET, setting Vault...")
    with pytest.raises(ValueError):
        latest_contract.setVault(
            collectionVault,
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            },
        )
    print("Vault NOT SET, setting Token Redeems Limit...")
    with pytest.raises(ValueError):
        latest_contract.setTokenRedeemsLimit(
            redeemsLimitPerToken,
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            },
        )
    print("Token Redeems Limit NOT SET, setting Mints per transaction...")
    with pytest.raises(ValueError):
        latest_contract.setMintablePerTransaction(
            mintsPerTransaction,
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            },
        )
    print("Mints per transaction NOT SET, setting mint -->OFF<--")
    with pytest.raises(ValueError):
        latest_contract.setMintActive(
            False,
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            },
        )
    print("Mint config NOT SET, DIDN'T SET ANYTHING! test pass!!")


###
# Test Mint Functionality
###

# Contract owner can set up a period of time to mint (Successful mint time)
def test_owner_set_right_time(succeedTestTime, latest_contract, developer):
    print(f"Setting sale period...")
    starts = succeedTestTime[0]
    print(f"Starts ==> {datetime.fromtimestamp(starts)}")
    ends = succeedTestTime[1]
    print(f"Ends ==> {datetime.fromtimestamp(ends)}")
    latest_contract.setSalePeriod(starts, ends, {"from": developer})
    print("Time set, asserting times...")
    assert latest_contract.startDate({"from": developer}) == starts
    assert latest_contract.endDate({"from": developer}) == ends
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Go!")


# Test user can't mint if mint is not active even within the mint period
def test_mint_correct_time_mint_not_active(latest_contract, developer, gas_failed_tx):
    print("Minting test... It must fail since the mint is not active...")
    with pytest.raises(ValueError):
        latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Contract owner can set Mint Active
def test_owner_can_set_mint_active(latest_contract, developer):
    print("Setting mint -->ON<--")
    latest_contract.setMintActive(True, {"from": developer})
    print("Mint set -->ON<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Assert configuration")
    assert latest_contract.isActive({"from": developer}) == True


# Test user can mint if is within a given period of time and the mint is active
def test_mint_correct_time_mint_active(latest_contract, developer):
    print("Minting test... You can mint!")
    latest_contract.mint(
        1,
        {
            "from": developer,
            "value": Web3.toWei(0.01, "ether"),
        },
    )


# Contract owner can set up a period of time to mint (Unsuccessful mint time - Mint Ended)
def test_owner_can_set_incorrect_time_ended(
    failTestTimeEnded, latest_contract, developer
):
    print(f"Setting sale period...")
    starts = failTestTimeEnded[0]
    print(f"Starts ==> {datetime.fromtimestamp(starts)}")
    ends = failTestTimeEnded[1]
    print(f"Ends ==> {datetime.fromtimestamp(ends)}")
    latest_contract.setSalePeriod(starts, ends, {"from": developer})
    print("Time set, asserting times...")
    assert latest_contract.startDate({"from": developer}) == starts
    assert latest_contract.endDate({"from": developer}) == ends
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Go!")


# Test user can not mint if the mint sale is active but the period of time is correct
def test_mint_incorrect_time_ended_mint_active(
    latest_contract, developer, gas_failed_tx
):
    print("Minting test... It must fail since the mint already ended...")
    with pytest.raises(ValueError):
        latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Contract owner can set mint not active
def test_owner_can_set_mint_not_active(latest_contract, developer):
    print("Setting mint -->OFF<--")
    latest_contract.setMintActive(False, {"from": developer})
    print("Mint set --OFF<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Assert configuration")
    assert latest_contract.isActive({"from": developer}) == False


# Test user can not mint if the mint is not active and the mint time ended
def test_mint_incorrect_time_mint_not_active(latest_contract, developer, gas_failed_tx):
    print(
        "Minting test... It must fail since the mint is not active and the time has ended..."
    )
    with pytest.raises(ValueError):
        latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Contract owner can set up a period of time to mint (Unsuccessful mint time - Mint Not Started)
def test_owner_can_set_incorrect_time_not_yet_start(
    failTestTimeNotYetStart, latest_contract, developer
):
    print(f"Setting sale period...")
    starts = failTestTimeNotYetStart[0]
    print(f"Starts ==> {datetime.fromtimestamp(starts)}")
    ends = failTestTimeNotYetStart[1]
    print(f"Ends ==> {datetime.fromtimestamp(ends)}")
    latest_contract.setSalePeriod(starts, ends, {"from": developer})
    print("Time set, asserting times...")
    assert latest_contract.startDate({"from": developer}) == starts
    assert latest_contract.endDate({"from": developer}) == ends
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Go!")


# Test user can't mint if the Sales period doesnt start yet
def test_mint_incorrect_time_ended_mint_not_active(
    latest_contract, developer, gas_failed_tx
):
    print(
        "Minting test... It must fail since the mint is not yet started and mint is not active..."
    )
    with pytest.raises(ValueError):
        latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Test user can't mint if the Sales period doesnt start yet with mint active
def test_mint_incorrect_time_ended_mint_active(
    latest_contract, developer, gas_failed_tx
):
    print("Setting mint -->ON<--")
    latest_contract.setMintActive(True, {"from": developer})
    print("Mint set -->ON<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Minting test... It must fail since the mint is not yet started...")
    with pytest.raises(ValueError):
        latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Contract owner can set infinite time sales period
def test_owner_can_set_infinite_time(
    succeedTestTimeAlwaysOpen, latest_contract, developer
):
    print(f"Setting sale period...")
    starts = succeedTestTimeAlwaysOpen[0]
    print(f"Starts ==> {datetime.fromtimestamp(starts)}")
    ends = succeedTestTimeAlwaysOpen[1]
    print(f"Ends ==> {datetime.fromtimestamp(ends)}")
    latest_contract.setSalePeriod(starts, ends, {"from": developer})
    print("Time set, asserting times...")
    assert latest_contract.startDate({"from": developer}) == starts
    assert latest_contract.endDate({"from": developer}) == ends
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Go!")


# Test user can mint if the sales period is set 0 - 0 (always can mint)
def test_mint_correct_time_mint_active(latest_contract, developer):
    print("Minting test... You have infinite time to mint!")
    latest_contract.mint(
        1,
        {
            "from": developer,
            "value": Web3.toWei(0.01, "ether"),
        },
    )


# Test user cant mint if the sales period is infinite but the mint is not active
def test_mint_infinite_time_mint_not_active(latest_contract, developer, gas_failed_tx):
    print("Setting mint -->OFF<--")
    latest_contract.setMintActive(False, {"from": developer})
    print("Mint set --OFF<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Minting test... You Can't mint even with your time!!")
    with pytest.raises(ValueError):
        latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Test user can't mint over the max mints per transaction (limit 4)
def test_mint_too_many_tokens(latest_contract, developer, gas_failed_tx):

    print("Minting test... You Can't mint that many tokens at once!!")
    with pytest.raises(ValueError):
        latest_contract.mint(
            5,
            {
                "from": developer,
                "value": Web3.toWei(0.05, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


# Test user can't mint if the eth sent is not enough
def test_mint_not_enough_eth(latest_contract, developer, gas_failed_tx):
    print("Minting test... Will Fail!! You need to spend more eth!!")
    with pytest.raises(ValueError):
        latest_contract.mint(
            4,
            {
                "from": developer,
                "value": Web3.toWei(0.03, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )


###
# Test Crowdfund Goals and Redeems Functionality ---> ETH_RAISED
###

# Test that contract owner can set a crowdfund method --> ETH_RAISED
def test_contract_owner_can_set_crowdfund_method_ETH_RAISED(developer, latest_contract):
    print("setting Crowdfund method ==> ETH_RAISED")
    latest_contract.setCrowdfundMethod(1, {"from": developer})


# Test that contract owner can configure a ETH_RAISED goal
def test_contract_owner_can_set_ETH_RAISED_goal(developer, latest_contract):
    print("setting Crowdfund Goal ==> ETH_RAISED ===> .1 ETH")
    with pytest.raises(ValueError):
        latest_contract.setCrowdfundGoal(
            0.1,
            {"from": developer},
        )


# Test that an user can't redeem when the ETH_RAISED goal is not met
def test_owner_cant_redeem_ETH_goal_not_met(developer, latest_contract, gas_failed_tx):
    balance = latest_contract.balance({"from": developer})
    print(f"Current raised funds ==> {balance}")
    print("Redeem... It must fail since the goal is not met yet")
    latest_contract.redeem(
        1,
        {
            "from": developer,
            "gas_limit": gas_failed_tx,
        },
    )


# Send ETH to the contract to hit the ETH_RAISED goal
def tester_sends_eth_to_met_goal()
latest_contract.mint(
            1,
            {
                "from": developer,
                "value": Web3.toWei(0.01, "ether"),
                "gas_limit": gas_failed_tx,
            },
        )

# test user can redeem if the goal was hit

# Test user can read the set goal

###
# Test Crowdfund Goals and Redeems Functionality ---> MINT_NUMBER
###

# Test that contract owner can set a crowdfund method --> MINT_NUMBER
def test_owner_can_set_crowdfund_method(developer, latest_contract):
    print("setting Crowdfund Goal ==> ETH_RAISED")
    latest_contract.setCrowdfundGoal(1, {"from": developer})


# test that an user can configure a threshold for the MINT_NUMBER goal

# test that an user can't redeem when the MINT_NUMBER goal is not met

# Mint tokens to hit the MINT_NUMBER goal

# test that an user can redeem when the MINT_NUMBER goal is hit

###
# Test Crowdfund Goals and Redeems Functionality ---> Safety
###

# Test that an user can configure a crowdfund method --> ETH_RAISED
def test_owner_can_set_crowdfund_method(developer, latest_contract):
    print("setting Crowdfund Goal ==> DEFAULT")
    latest_contract.setCrowdfundGoal(0, {"from": developer})


# test that an user can't redeem when the croudfund method is set at "default"

# Test user can't redeem over his "Redeems per token limit"

# Test that only the token owner can redeem with his token

###
# Test General Management Functions
###

# Test that a Bad actor can't withdraw the funds

# test that the contract owner can withdraw the contract raised funds to the vault
