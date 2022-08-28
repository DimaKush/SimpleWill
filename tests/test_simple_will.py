import datetime
import time

import brownie


def get_new_release_time(_test_delay):
    return datetime.datetime.timestamp(datetime.datetime.now() 
    + datetime.timedelta(seconds=_test_delay))  


def wait_release_time(_contract):
    seconds_before_release = _contract.getReleaseTime() - datetime.datetime.timestamp(datetime.datetime.now())
    if seconds_before_release > 0:
        time.sleep(seconds_before_release)


def test_simple_will_contract_deploy(deployer, simple_will_contract):
    """
    Test if the contract is correctly deployed.
    """
    owner = simple_will_contract.owner({"from": deployer})
    assert owner == deployer


def test_new_release_time(deployer, simple_will_contract, test_delay):
    """
    Test if the release time variable can be changed.
    """
    new_release_time = get_new_release_time(test_delay)

    simple_will_contract.setNewReleaseTime(new_release_time, {'from': deployer})
    assert simple_will_contract.getReleaseTime() == new_release_time


def test_set_new_beneficiary(deployer, executor, simple_will_contract):
    """
    Test if the beneficiary address can be changed.
    """
    simple_will_contract.setNewBeneficiary(executor, {'from': deployer})
    assert simple_will_contract.getBeneficiary() == executor
    with brownie.reverts():
        simple_will_contract.setNewBeneficiary(executor, {'from': executor})


def test_release_ERC20(simple_will_contract, deployer, beneficiary, executor, ERC20_token_contracts, test_delay):
    new_release_time = get_new_release_time(test_delay)
    simple_will_contract.setNewReleaseTime(new_release_time, {'from': deployer})
    for ERC20_token_contract in range(len(ERC20_token_contracts)):
        with brownie.reverts():
            simple_will_contract.releaseERC20(ERC20_token_contracts[ERC20_token_contract], {'from': executor})

    wait_release_time(simple_will_contract)
    for ERC20_token_contract in range(len(ERC20_token_contracts)):
        deployer_balance = ERC20_token_contracts[ERC20_token_contract].balanceOf(deployer)
        simple_will_contract.releaseERC20(ERC20_token_contracts[ERC20_token_contract], {'from': executor})
        assert ERC20_token_contracts[ERC20_token_contract].balanceOf(deployer) == 0
        assert ERC20_token_contracts[ERC20_token_contract].balanceOf(beneficiary) == deployer_balance


def test_release_ERC721(simple_will_contract, deployer, beneficiary, executor, ERC721_token_contracts, n_ids, test_delay):
    new_release_time = get_new_release_time(test_delay)
    simple_will_contract.setNewReleaseTime(new_release_time, {'from': deployer})

    for ERC721_token_contract in range(len(ERC721_token_contracts)):
        with brownie.reverts():
            simple_will_contract.releaseERC721(ERC721_token_contracts[ERC721_token_contract], list(range(n_ids)), {'from': executor})

    wait_release_time(simple_will_contract)
    for ERC721_token_contract in range(len(ERC721_token_contracts)):
        deployer_balance = ERC721_token_contracts[ERC721_token_contract].balanceOf(deployer)
        simple_will_contract.releaseERC721(ERC721_token_contracts[ERC721_token_contract], list(range(n_ids)), {'from': executor})
        assert ERC721_token_contracts[ERC721_token_contract].balanceOf(deployer) == 0
        assert ERC721_token_contracts[ERC721_token_contract].balanceOf(beneficiary) == deployer_balance


def test_release_ERC1155(simple_will_contract, deployer, beneficiary, value, ERC1155_token_contracts, executor, n_ids, test_delay):
    new_release_time = get_new_release_time(test_delay)
    simple_will_contract.setNewReleaseTime(new_release_time, {'from': deployer})
    for ERC1155_token_contract in ERC1155_token_contracts:
        with brownie.reverts():
            simple_will_contract.releaseERC1155(ERC1155_token_contract, list(range(n_ids)), [value] * n_ids,  {'from': executor})
    wait_release_time(simple_will_contract)
    for ERC1155_token_contract in ERC1155_token_contracts:
        simple_will_contract.releaseERC1155(ERC1155_token_contract, list(range(n_ids)), [value] * n_ids,  {'from': executor})
        for id in range(n_ids):
            assert ERC1155_token_contract.balanceOf(deployer, id) == 0
            assert ERC1155_token_contract.balanceOf(beneficiary, id) == value


def test_batch_release(simple_will_contract,
                       ERC20_token_contracts,
                       ERC721_token_contracts,
                       ERC1155_token_contracts, n_ids, n_contracts, value, deployer, beneficiary, test_delay):
    new_release_time = get_new_release_time(test_delay)
    simple_will_contract.setNewReleaseTime(new_release_time, {'from': deployer})
    with brownie.reverts():
        simple_will_contract.batchRelease(
            list(ERC20_token_contracts),
            list(ERC721_token_contracts),
            list(ERC1155_token_contracts),
            [list(range(n_ids))] * n_contracts,
            [list(range(n_ids))] * n_contracts,
            [[value] * n_ids] * n_contracts,
            {'from': deployer}
        )
    wait_release_time(simple_will_contract)
    simple_will_contract.batchRelease(
        list(ERC20_token_contracts),
        list(ERC721_token_contracts),
        list(ERC1155_token_contracts),
        [list(range(n_ids))] * n_contracts,
        [list(range(n_ids))] * n_contracts,
        [[value] * n_ids] * n_contracts,
        {'from': deployer}
    )
    for ERC20_token_contract in ERC20_token_contracts:
        assert ERC20_token_contract.balanceOf(deployer) == 0
        assert ERC20_token_contract.balanceOf(beneficiary) == value

    for ERC721_token_contract in ERC721_token_contracts:
        beneficiary_balance = ERC721_token_contract.balanceOf(beneficiary)
        assert ERC721_token_contract.balanceOf(deployer) == 0
        assert beneficiary_balance == n_ids

    for ERC1155_token_contract in ERC1155_token_contracts:
        for id in range(n_ids):
            beneficiary_balance = ERC1155_token_contract.balanceOf(beneficiary, id)
            assert ERC1155_token_contract.balanceOf(deployer, id) == 0
            assert beneficiary_balance == value
