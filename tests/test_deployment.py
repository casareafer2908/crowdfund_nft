import pytest
from datetime import datetime
import pytz
import time
from brownie import OneTMShowOff, accounts, network, config
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


@pytest.fixture
def redeemable_token_id(developer, latest_contract):
    latest_contract


###
# Test Contract Deployment
###

# Test that the contract deploys successfully
@pytest.mark.timeout(200)
def test_contract_deployment(rinkeby_test_contract, setPrice, setSupply, developer):
    print(f"Assert that the price set is correct...")
    assert rinkeby_test_contract.price({"from": developer}) == setPrice
    print(f"Assert that the supply limit is correct...")
    assert rinkeby_test_contract.supplyLimit({"from": developer}) == setSupply
    print("Done!")


# Test that the contract cant be configured by Bad Actors
@pytest.mark.timeout(200)
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
@pytest.mark.timeout(200)
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
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
def test_owner_can_set_mint_active(latest_contract, developer):
    print("Setting mint -->ON<--")
    latest_contract.setMintActive(True, {"from": developer})
    print("Mint set -->ON<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Assert configuration")
    assert latest_contract.isActive({"from": developer}) == True


# Test user can mint if is within a given period of time and the mint is active
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
def test_owner_can_set_incorrect_time_ended(
    failTestTimeEnded, latest_contract, developer
):
    print(f"Setting sale period...")
    starts = int(failTestTimeEnded[0])
    print(f"Starts ==> {datetime.fromtimestamp(starts)}")
    ends = int(failTestTimeEnded[1])
    print(f"Ends ==> {datetime.fromtimestamp(ends)}")
    latest_contract.setSalePeriod(starts, ends, {"from": developer})
    print("Time set, asserting times...")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    assert latest_contract.startDate({"from": developer}) == starts
    assert latest_contract.endDate({"from": developer}) == ends


# Test user can not mint if the mint sale is active but the period of time is correct
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
def test_owner_can_set_mint_not_active(latest_contract, developer):
    print("Setting mint -->OFF<--")
    latest_contract.setMintActive(False, {"from": developer})
    print("Mint set --OFF<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Assert configuration")
    assert latest_contract.isActive({"from": developer}) == False


# Test user can not mint if the mint is not active and the mint time ended
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
def test_mint_infinite_time_mint_active(latest_contract, developer):
    print("Minting test... You have infinite time to mint!")
    latest_contract.mint(
        1,
        {
            "from": developer,
            "value": Web3.toWei(0.01, "ether"),
        },
    )


# Test user cant mint if the sales period is infinite but the mint is not active
@pytest.mark.timeout(100)
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
@pytest.mark.timeout(100)
def test_mint_too_many_tokens(latest_contract, developer, gas_failed_tx):
    print("Setting mint -->ON<--")
    latest_contract.setMintActive(True, {"from": developer})
    print("Mint set --ON<--")
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
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
@pytest.mark.timeout(100)
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

###
# To test redeems, first you need to get the tokens owned by the tester wallet,
# choose one of those tokens with remaining redeems, then call redeem with that
# token id
###

# Test that contract owner can set a crowdfund method --> ETH_RAISED
@pytest.mark.timeout(100)
def test_contract_owner_can_set_crowdfund_method_ETH_RAISED(developer, latest_contract):
    print("setting Crowdfund method ==> ETH_RAISED")
    latest_contract.setCrowdfundMethod(0, {"from": developer})
    assert latest_contract.crowdfund_method({"from": developer}) == 0


# Test that contract owner can configure a ETH_RAISED goal
@pytest.mark.timeout(100)
def test_contract_owner_can_set_ETH_RAISED_goal(developer, latest_contract):
    print("setting Crowdfund Goal ==> ETH_RAISED ===> .1 ETH")
    goal = Web3.toWei(0.1, "ether")
    latest_contract.setCrowdfundGoal(
        goal,
        {"from": developer},
    )
    assert latest_contract.goal({"from": developer}) == goal


# Test user can read the set goal
@pytest.mark.timeout(100)
def test_user_can_read_set_goal(developer, latest_contract):
    assert latest_contract.goal({"from": developer}) == Web3.toWei(0.1, "ether")


# Test that an user can't redeem when the ETH_RAISED goal is not met
@pytest.mark.timeout(100)
def test_owner_cant_redeem_ETH_goal_not_met(developer, latest_contract, gas_failed_tx):
    balance = latest_contract.balance()
    print(f"Current raised funds ==> {balance}")
    print("Redeem... It must fail since the goal is not met yet")
    with pytest.raises(ValueError):
        latest_contract.redeem(
            0,
            1,
            {
                "from": developer,
                "gas_limit": gas_failed_tx,
            },
        )


# Mint tokens to hit ETH_RAISED goal
@pytest.mark.timeout(100)
def tester_mints_to_met_goal_ETH_RAISED(latest_contract, developer):
    print("set max mints to 10 to Raise funds faster")
    balance = latest_contract.balance()
    print(f"Current raised funds ==> {Web3.fromWei(balance, 'ether')} ETH")
    latest_contract.setMintablePerTransaction(10, {"from": developer})
    print("wait 5 secs for blockchain to update")
    time.sleep(5)
    print("Minting 10 tokens...")
    latest_contract.mint(
        10,
        {
            "from": developer,
            "value": Web3.toWei(0.10, "ether"),
        },
    )
    balance = latest_contract.balance()
    print(f"Current raised funds ==> {Web3.fromWei(balance, 'ether')} ETH")


# Test user can redeem if the goal was hit
@pytest.mark.timeout(100)
def test_token_owner_can_redeem_ETH_goal_met(developer, latest_contract):
    balance = latest_contract.balance()
    print(f"Current raised funds ==> {Web3.fromWei(balance, 'ether')} ETH")
    print("Redeem... It should succeed since the goal is met")
    goal = latest_contract.goal({"from": developer})
    print(f"the goal ==> {Web3.fromWei(goal, 'ether')}")
    latest_contract.redeem(0, 1, {"from": developer})


# Test user can't redeem if he has no redeems left with the ETH GOAL met
@pytest.mark.timeout(100)
def test_token_owner_cant_redeem_ETH_goal_met_no_redeems_left(
    developer, latest_contract, gas_failed_tx
):
    balance = latest_contract.balance()
    print(f"Current raised funds ==> {Web3.fromWei(balance, 'ether')} ETH")
    print("Redeem... It should fail since token 0 got no redeems left")
    goal = latest_contract.goal({"from": developer})
    print(f"the goal ==> {Web3.fromWei(goal, 'ether')}")
    with pytest.raises(ValueError):
        latest_contract.redeem(
            0,
            1,
            {
                "from": developer,
                "gas_limit": gas_failed_tx,
            },
        )


###
# Test Crowdfund Goals and Redeems Functionality ---> MINT_NUMBER
###

# Test that contract owner can set a crowdfund method --> MINT_NUMBER
@pytest.mark.timeout(100)
def test_owner_can_set_crowdfund_method_MINT_NUMBER(developer, latest_contract):
    print("Setting Crowdfund method ==> MINT_NUMBER")
    latest_contract.setCrowdfundMethod(1, {"from": developer})
    assert latest_contract.crowdfund_method({"from": developer}) == 1


# Test contract owner can configure the MINT_NUMBER goal
@pytest.mark.timeout(100)
def test_contract_owner_can_set_MINT_NUMBER_goal(developer, latest_contract):
    print("setting Crowdfund Goal ==> MINT_NUMBER ===> 20 NFT's")
    goal = 20
    latest_contract.setCrowdfundGoal(
        goal,
        {"from": developer},
    )
    assert latest_contract.goal({"from": developer}) == goal


# Contract owner can set redeem state false
@pytest.mark.timeout(100)
def contract_owner_sets_redeem_state_false(latest_contract, developer):
    print("setting state false for testing...")
    latest_contract.setRedeemState(False, {"from": developer})
    time.sleep(1)
    assert latest_contract.readRedeemState() == False


# Test user can't redeem when the MINT_NUMBER goal is not met
@pytest.mark.timeout(100)
def test_owner_cant_redeem_MINT_NUMBER_goal_not_met(
    developer, latest_contract, gas_failed_tx
):
    minted = latest_contract.totalSupply()
    print(f"Current minted nft's ==> {minted}")
    goal = latest_contract.goal({"from": developer})
    print(f"the goal ==> {goal}")
    print("Redeem... It must fail since the mint number goal is not met yet")
    with pytest.raises(ValueError):
        latest_contract.redeem(
            1,
            1,
            {
                "from": developer,
                "gas_limit": gas_failed_tx,
            },
        )


# Mint tokens to hit the MINT_NUMBER goal
@pytest.mark.timeout(100)
def tester_mints_to_met_goal_MINT_NUMBER(latest_contract, developer):
    minted = latest_contract.totalSupply()
    print(f"Current minted nft's ==> {minted}")
    print("Minting 10 tokens...")
    latest_contract.mint(
        10,
        {
            "from": developer,
            "value": Web3.toWei(0.10, "ether"),
        },
    )
    time.sleep(1)
    minted = latest_contract.totalSupply()
    print(f"Current minted nft's ==> {minted}")


# test that an user can redeem when the MINT_NUMBER goal is hit
@pytest.mark.timeout(100)
def test_token_owner_can_redeem_MINT_NUMBER_goal_met(developer, latest_contract):
    minted = latest_contract.totalSupply()
    print(f"Current minted nft's ==> {minted}")
    goal = latest_contract.goal({"from": developer})
    print(f"the goal ==> {goal}")
    print("Redeem... It should succeed since the goal is met")
    latest_contract.redeem(2, 1, {"from": developer})


# Test user can't redeem over his "Redeems per token limit"
@pytest.mark.timeout(100)
def test_owner_cant_redeem_over_redeem_limit(developer, latest_contract, gas_failed_tx):
    print("Redeem... It must fail since the redeem limit is 1 per token")
    with pytest.raises(ValueError):
        latest_contract.redeem(
            2,
            2,
            {
                "from": developer,
                "gas_limit": gas_failed_tx,
            },
        )


###
# Test Crowdfund Goals and Redeems Functionality ---> Safety
###

# Test that an user can configure a crowdfund method --> DEFAULT
@pytest.mark.timeout(100)
def test_owner_can_set_crowdfund_method_DEFAULT(developer, latest_contract):
    print("Setting Crowdfund Goal ==> DEFAULT")
    latest_contract.setCrowdfundMethod(0, {"from": developer})
    assert latest_contract.crowdfund_method({"from": developer}) == 0


# Test user can't redeem when the croudfund method is set at "default"
@pytest.mark.timeout(100)
def test_owner_cant_redeem_crowdfund_metod_DEFAULT(
    developer, latest_contract, gas_failed_tx
):
    print("Redeem... It must fail since the crowdfund method is DEFAULT")
    with pytest.raises(ValueError):
        latest_contract.redeem(
            2,
            1,
            {
                "from": developer,
                "gas_limit": gas_failed_tx,
            },
        )


# Test that only the token owner can redeem with his token
@pytest.mark.timeout(100)
def test_BAD_ACTOR_cant_redeem_not_owned_token(
    badActor, latest_contract, gas_failed_tx
):
    print("Redeem... It must fail since BADACTOR is not owner of the token")
    with pytest.raises(ValueError):
        latest_contract.redeem(
            4,
            1,
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            },
        )


###
# Test General Management Functions
###

# Test that a Bad actor can't withdraw the funds
@pytest.mark.timeout(100)
def test_BAD_ACTOR_cant_withdraw_funds_from_the_contract(
    badActor, latest_contract, gas_failed_tx
):
    print("Withdraw... It must fail since BADACTOR is not owner of the contract")
    with pytest.raises(ValueError):
        latest_contract.withdraw(
            {
                "from": badActor,
                "gas_limit": gas_failed_tx,
            }
        )


# test that the contract owner can withdraw the contract raised funds to the vault
@pytest.mark.timeout(100)
def test_owner_can_withdraw_funds_to_the_vault(
    developer, latest_contract, gas_failed_tx
):
    print("Withdraw funds to the vault... it should pass since im the owner")
    latest_contract.withdraw({"from": developer})
