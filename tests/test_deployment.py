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
    startTime = datetime.datetime(
        2022, 5, 20, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    endTime = datetime.datetime(
        2022, 5, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    return [startTime, endTime]


@pytest.fixture
def failTestTimeEnded():
    startTime = datetime.datetime(
        2022, 5, 10, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    endTime = datetime.datetime(
        2022, 5, 15, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    return [startTime, endTime]


@pytest.fixture
def succeedTestTime():
    startTime = datetime(2022, 5, 17, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    endTime = datetime(2022, 7, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei"))
    return [startTime.timestamp(), endTime.timestamp()]


@pytest.fixture
def alwaysActiveTestTime():
    startTime = 0
    endTime = 0
    return [startTime, endTime]


@pytest.fixture
def mintsPerTransaction():
    return 3


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
    print(f"Deployed Contract address ==> {rinkeby_test_contract.address}")
    print(f"Assert that the price set is correct...")
    assert rinkeby_test_contract.price({"from": developer}) == setPrice
    print(f"Assert that the supply limit is correct...")
    assert rinkeby_test_contract.supplyLimit({"from": developer}) == setSupply
    print("Done!")


# Test that the contract is successfully configured
def test_contract_configuration(
    latest_contract,
    developer,
    redeemsLimitPerToken,
    metadataLibrary,
    mintsPerTransaction,
    collectionVault,
):
    print(f"Used Contract address ==> {latest_contract.address}")
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
    print("Mint set -->OFF<--")
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


###
# Test Mint Functionality
###

# Test user can set up a period of time to mint (Successful mint time)


def test_contract_owner_can_set_mint_period(
    succeedTestTime, latest_contract, developer
):
    print(f"Used Contract address ==> {latest_contract.address}")
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


# Test user cant mint if the mint sale is not active even if the period of time
def test_mint_within_a_given_time(latest_contract, developer, gas_failed_tx):
    print(f"Used Contract address ==> {latest_contract.address}")
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


# Test user can mint if is within a given period of time and the mint is active

# Test that an user can mint within a period of given time

# test that an user can't mint if the Sales period doesnt start yet

# test that an user can't mint if the Sales period is over

# test that an user can mint if the sales period is set 0 - 0 (always can mint)

# test that an user can't mint over the max mints per transaction

# test that an user can mint less than the Max Mints per transaction

###
# Test Crowdfund Goals Functionality
###

# test that an user can configure a crowdfund method --> Default

# test that an user can't redeem when the croudfund method is set at "default"

# test that an user can configure a crowdfund method --> Eth raised

# test that an user can set a goal for eth raised

# test that an user can redeem when the goal is met

# test that an user can't redeem when the ETH goal is not met (change the goal to a higher value)

# test that an user can set a crowdfund method of minted tokens

# test that an user can set a goal for total minted tokens

# test that an user can redeem when the minted tokens goal is met

# test that an user can't redeem when the minted tokens goal is not met (change the goal to a higher value)

# test that an user can redeem over his "Redeems per token limit"

###
# Test General Management Functions
###

# test that the contract owner can withdraw the contract raised funds to the vault
