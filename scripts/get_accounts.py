from brownie import accounts, network, config


def get_accounts():
    if network.show_active() == 'development':
        deployer = accounts[0]
        beneficiary = accounts[1]
        executor = accounts[2]
    else:
        try:
            deployer = accounts.add(config['wallets']['deployer'])
            beneficiary = accounts.add(config['wallets']['beneficiary'])
            executor = accounts.add(config['wallets']['executor'])
        except FileNotFoundError:
            deployer = accounts.add(input("Add deployer account form private key: "))
            beneficiary = accounts.add(input("Add beneficiary account form private key: "))
            executor = accounts.add(input("Add executor account form private key: "))
    return deployer, beneficiary, executor
