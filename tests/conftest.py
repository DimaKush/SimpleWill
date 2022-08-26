import datetime
from brownie import config
import brownie.network
import pytest



@pytest.fixture(scope='function', autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass


@pytest.fixture(scope='module')
def n_contracts():
    yield config['settings']['n_contracts']


@pytest.fixture(scope='module')
def value():
    yield config['settings']['value']


@pytest.fixture(scope='module')
def n_ids():
    yield config['settings']['n_ids']


@pytest.fixture(scope='module')
def deployer(accounts):
    deployer = accounts[0]
    yield deployer


@pytest.fixture(scope='module')
def beneficiary(accounts):
    beneficiary = accounts[1]
    yield beneficiary


@pytest.fixture(scope='module')
def executor(accounts):
    executor = accounts[2]
    yield executor


@pytest.fixture(scope='module')
def ERC20_token_contracts(deployer, TokenERC20, n_contracts, value):
    """
    :yield: instances of ERC20 contracts
    """
    for i in range(n_contracts):
        TokenERC20.deploy(value,
                          f"TokenERC20_{i}",
                          f"T20_{i}",
                          {'from': deployer})
    yield TokenERC20


@pytest.fixture(scope='module')
def ERC721_token_contracts(deployer, TokenERC721, n_contracts, n_ids):
    for i in range(n_contracts):
        deployed_contract = TokenERC721.deploy(
            f"TokenERC721_{i}",
            f"T721_{i}",
            {'from': deployer}
        )
        for u in range(n_ids):
            deployed_contract.safeMint(deployer,
                                       f"someuri_{u}",
                                       {'from': deployer})
    yield TokenERC721


@pytest.fixture(scope='module')
def ERC1155_token_contracts(deployer, TokenERC1155, value, n_contracts, n_ids):
    for i in range(n_contracts):
        deployed_contract = TokenERC1155.deploy(
            f"https://somelink.eth.link/ERC1155_{i}.json",
            {'from': deployer}
        )
        for u in range(n_ids):
            deployed_contract.mint(deployer, u, value, "")
    print(TokenERC1155)
    yield TokenERC1155


@pytest.fixture(scope='module', autouse=True)
def will_contract(deployer, beneficiary, SimpleWill, ERC20_token_contracts, ERC721_token_contracts,
                  ERC1155_token_contracts):
    release_time = round(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(seconds=config['settings']['test_delay'])))
    contract = deployer.deploy(
        SimpleWill,
        beneficiary,
        release_time
    )
    yield contract


@pytest.fixture(scope="module", autouse=True)
def batch_approve(deployer, ERC20_token_contracts, ERC721_token_contracts, ERC1155_token_contracts, will_contract, value):
    for i in ERC20_token_contracts:
        i.approve(will_contract.address, value, {'from': deployer})
    for i in ERC721_token_contracts:
        i.setApprovalForAll(will_contract.address, True, {'from': deployer})
    for i in ERC1155_token_contracts:
        i.setApprovalForAll(will_contract.address, True, {'from': deployer})

