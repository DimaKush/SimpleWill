# Simple Will contract

Delayed recovery tool for ERC20, ERC721 and ERC1155 tokens.
Contract is used as a will: delpoyer of contract allow tokens to SimpleWill that can be tranfered from deployer to beneficiary
only after release time. Testator should extend release time to prove his access to account. When release time is passed, anybody can call release functions to proceed wills logic. 

## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html).

2. Clone this repo 
   ```
   git clone https://github.com/DimaKush/SimpleWill
   cd SimpleWill
   ```

2. Install [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts) packages

   ```bash
   brownie pm install OpenZeppelin/openzeppelin-contracts@4.7.3
   ```

3. If you want to deploy on testnets, do the following.

   Set our environment variables to a .env file. You can use the .env_example in this repo
   as a template, just fill in the values and rename it to '.env'.

## Usage

1. Open the Brownie console. Starting the console launches a fresh [Ganache](https://www.trufflesuite.com/ganache) instance in the background.

   ```bash
   brownie console
   ```

   Alternatively, to run on Goeri, set the network flag to goerli

   ```bash
   brownie console --network goerli
   ```

2. Run the [deployment script](scripts/deploy_SimpleWill.py) to deploy the project's smart contracts using Brownie console:

   ```python
   >>> run("deploy_SimpleWill")
   ```
   Or in terminal:

   ```bash
   brownie run deploy_SimpleWill --network goerli
   ```

   Replace `goerli` with the name of the network you wish you use. You may also wish to adjust Brownie's [network settings](https://eth-brownie.readthedocs.io/en/stable/network-management.html).

4. Interact with the smart contract using Brownie console:

   ```python
   # set new release time
   >>> SimpleWill[-1].setNewReleaseTime(1661455347, {'from': accounsts[0]})
   # see workflow
   >>> run('deploy_and_release_SimpleWill')
   ```
### Configuring

Configure settings at 'brownie-config.yaml'

### Testing

To run the test suite:

```bash
brownie test
```

## Resources

[Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/)

["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99)

[Patrick Collins](https://twitter.com/PatrickAlphaC) tutorial on [youtube](https://www.youtube.com/watch?v=M576WGiDBdQ&t=43350s)

[Brownie Mixes](https://github.com/brownie-mix)

[OpenZeppelin docs](https://docs.openzeppelin.com/)


## License

Distributed under the [MIT License](https://github.com/DimaKush/SimpleWill/blob/master/LICENSE)

