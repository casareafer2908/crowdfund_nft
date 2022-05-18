import pytest
import datetime
import pytz
from brownie import OneTMShowOff, accounts, network, config
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
def payableAmmount(mintAmmount):
    return mintAmmount * 0.01

@pytest.fixture
def failTestTime():
    startTime = datetime.datetime(
    2022, 5, 20, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    endTime = datetime.datetime(
        2022, 5, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    return [startTime,endTime]

@pytest.fixture
def succeedTestTime():
    startTime = datetime.datetime(
    2022, 5, 17, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    endTime = datetime.datetime(
        2022, 5, 23, 3, 0, 0, 0, tzinfo=pytz.timezone("Asia/Taipei")
    )
    return [startTime,endTime]

@pytest.fixture
def alwaysActiveTestTime():
    startTime = 0
    endTime = 0
    return [startTime,endTime]

@pytest.fixture
def mintsPerWallet():
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
        {"from": developer},
        publish_source=get_publish_source(),
    )
    print(f"Contract deployed in address ==> {deployed.address}")
    return deployed


# Get the latest deployed contract
@pytest.fixture
def latest_contract(OneTMShowOff):
    contract = OneTMShowOff[len(OneTMShowOff) - 1]
    print (f"Used Contract address ==> {contract.address}")
    return contract


def test_contract_deployment(rinkeby_test_contract, setPrice, setSupply, developer):
    print(f"Deployed Contract address ==> {rinkeby_test_contract.address}")
    print(f"Assert that the price set is correct...")
    assert rinkeby_test_contract.price({"from": developer}) == setPrice
    print(f"Assert that the supply limit is correct...")
    assert rinkeby_test_contract.supplyLimit({"from": developer}) == setSupply
    print("Done!")

def test_contract_configuration(latest_contract,developer):
