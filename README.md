# Interview Showcase


This is a repo to work with and use NFTs smart contracts in a python environment. 

## Prerequisites

Please install or have installed the following:
- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```
Or, if that doesn't work, via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```

2. Clone this repo
```
https://github.com/casareafer2908/updated_deployer_mix_nft

```

1. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

If you want to be able to deploy to testnets, do the following. 

4. Set your environment variables

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You'll also need testnet rinkeby ETH and LINK. You can get LINK and ETH into your wallet by using the [rinkeby faucets located here](https://faucets.chain.link/rinkeby). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0)

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

Then, make sure your `brownie-config.yaml` has:

```
dotenv: .env
```

You can also [learn how to set environment variables easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html)


Or you can run the above in your shell. 

### You need to create a file .env to add your own test info

Example of .env file

```
### remove the '#' to use the environment variables
# Infura project id
 export WEB3_INFURA_PROJECT_ID=asdasdasdasd

# Test wallet key
 export PRIVATE_KEY=asdasdasdasd

#test wallet 2 key (I used this for tests)
 export PRIVATE_KEY_TEST=asdasdasd

# test wallet address
 export VAULT_ADDRESS=asdadasdasd

# chainling vrf consumer id  (not needed for show off)
# export VRF_SUBSCRIPTION_ID= asdasdasd

 export ETHERSCAN_TOKEN=asdasdasd

# export IPFS_URL=http://127.0.0.1:5001
# export UPLOAD_IPFS=true

# export PINATA_API_KEY='asdasdasdasd'
# export PINATA_API_SECRET='asdasdasdasd'
```


# Usage

There's 1 type of NFTs here. 
1. `ERC721.sol`

This contract mints an unique NFT tradeable in Opensea, the metadata is to be set via its scripts

You can 100% use the rinkeby testnet to see your NFTs rendered on opensea, but it's suggested that you test and build on a local development network so you don't have to wait as long for transactions. 

### Running Scripts

It needs a testnet. We default to rinkeby since that seems to be the testing standard for NFT platforms. You will need testnet rinkeby ETH and testnet Rinkeby LINK. You can find faucets for both in the [Chainlink documentation](https://docs.chain.link/docs/link-token-contracts#rinkeby). 


# To deploy and create nfts follow these steps

You'll need [testnet Rinkeby](https://faucet.rinkeby.io/) and [testnet LINK](https://rinkeby.chain.link/) in the wallet associated with your private key. 

Deploy:

```
brownie run scripts/deploy_oneTM_contracts.py --network rinkeby
```

Configure
```
brownie run scripts/configure_oneTM_collection.py --network rinkeby
```

then mint
```
brownie run scripts/mint_n_nfts.py --network rinkeby
```

# Verify on Etherscan

The simple contract and the advanced contract can be verified if you just set your `ETHERSCAN_TOKEN`. 

## Misc
There are some helpful scripts in `helpful_scripts.py`.

## Testing

```
brownie test -s --network rinkeby
```

## Linting

```
pip install black 
pip install autoflake
autoflake --in-place --remove-unused-variables -r .
black .
```

## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering. 
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

Shoutout to [TheLinkMarines](https://twitter.com/TheLinkMarines) on twitter for the puppies!

Any questions? Join our [Discord](https://discord.gg/2YHSAey)

## License

This project is licensed under the [MIT license](LICENSE).
