from brownie import accounts, network


def get_accounts():
    if network.show_active() == 'development':
        deployer = accounts[0]
        beneficiary = accounts[1]
    else:
        try:
            deployer = accounts.load('deployer')
            beneficiary = accounts.load('beneficiary')
        except FileNotFoundError:
            deployer = accounts.add(input("Add deployer account form private key: "))
            beneficiary = accounts.add(input("Add beneficiary account form private key: "))
    return deployer, beneficiary
