import datetime

from brownie import SimpleWill, config, network

from .get_accounts import get_accounts


def main():
    deployer, beneficiary, executor = get_accounts()
    release_time = round(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(seconds=config['settings']['delay'])))
    return SimpleWill.deploy(
        beneficiary,
        release_time,
        {'from': deployer},
        publish_source=config['networks'][network.show_active()]['verify']
    )
