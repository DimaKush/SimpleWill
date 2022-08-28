import time
from brownie import TokenERC20, TokenERC721, TokenERC1155, SimpleWill, config, network
import datetime
from scripts.get_accounts import get_accounts


def main():
    n_contracts = config['settings']['n_contracts']
    n_ids = config['settings']['n_ids']
    value = config['settings']['value']
    publish_source = config['networks'][network.show_active()]['verify']
    deployer, beneficiary, executor = get_accounts()
    
    for i in range(n_contracts):
        TokenERC20.deploy(value,
                          f"TokenERC20_{i}",
                          f"T20_{i}",
                          {'from': deployer},
                          publish_source=publish_source)
        TokenERC721.deploy(
            f"TokenERC721_{i}",
            f"T721_{i}",
            {'from': deployer},
            publish_source=publish_source
        )
        TokenERC1155.deploy(
            f"https://somelink.eth.link/ERC1155_{i}.json",
            {'from': deployer},
            publish_source=publish_source)
        for u in range(n_ids):
            TokenERC721[-1].safeMint(deployer, f"someuri_{u}", {'from': deployer})
            TokenERC1155[-1].mint(deployer, u, value, "", {'from': deployer})
    release_time = round(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(seconds=config['settings']['delay'])))
    SimpleWill.deploy(
        beneficiary,
        release_time,
        {'from': deployer},
        publish_source=publish_source
    )
    for i in TokenERC20:
        i.approve(SimpleWill[-1], 5, {'from': deployer})
    for i in TokenERC721:
        i.setApprovalForAll(SimpleWill[-1], True, {'from': deployer})
    for i in TokenERC1155:
        i.setApprovalForAll(SimpleWill[-1], True, {'from': deployer})

    time_before_release = SimpleWill[-1].getReleaseTime() - datetime.datetime.timestamp(datetime.datetime.now())
    if time_before_release > 0:
        time.sleep(time_before_release)
    SimpleWill[-1].batchRelease(
        list(TokenERC20),
        list(TokenERC721),
        list(TokenERC1155),
        [list(range(n_ids))] * n_contracts,
        [list(range(n_ids))] * n_contracts,
        [[value] * n_ids] * n_contracts,
        {'from': executor}
    )