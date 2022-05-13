from brownie import OneTMShowOff, accounts, config
from web3 import Web3


def main():
    dev = accounts.add(config["wallets"]["from_key"])

    # Get the latest deployed contract
    one_tm_show_off = OneTMShowOff[len(OneTMShowOff) - 1]
    ask_user(one_tm_show_off, dev)


def ask_user(one_tm_show_off, dev):
    contractBal = one_tm_show_off.balance()
    check = (
        str(
            input(
                f"Transfer Raised funds? ({Web3.fromWei(contractBal, 'ether')} Eth) (y/n): "
            )
        )
        .lower()
        .strip()
    )
    try:
        if check[0] == "y":
            print(
                f"Raised Funds ==> {Web3.fromWei(contractBal, 'ether')} Eth to be transfered to vault (address: {one_tm_show_off.vault()})"
            )
            one_tm_show_off.withdraw({"from": dev, "value": contractBal})
        elif check[0] == "n":
            print("Cancelled operation")
        else:
            print("Invalid Input")
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()
