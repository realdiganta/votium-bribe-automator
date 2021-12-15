from brownie import (
    accounts,
    interface,
    BribesManager,
    BribesLogic,
    BribesFactory
)
from config import (
    GAUGE_INDEX,
    TOKEN,
    TOKENS_PER_VOTE
)

PROPOSAL = "0xc26deaa05f45f3f6ad088cb6603d77cb2e826ff98b69e9a122706a37c8694681"


def test_gas_costs():
    token_whale = accounts.at(
        "0x63278bf9acdfc9fa65cfa2940b89a34adfbcb4a1", force=True)
    token = interface.IERC20(TOKEN)

    # deply the BribesLogic library first
    BribesLogic.deploy({"from": token_whale})

    # this will show the gas costs of directly deploying the BribesManager contract
    manager = BribesManager.deploy(
        TOKEN, GAUGE_INDEX, TOKENS_PER_VOTE,  {"from": token_whale})

    # send tokens for bribing
    token.transfer(manager, TOKENS_PER_VOTE * 2, {'from': token_whale})

    # bribe
    manager.sendBribe(PROPOSAL)

    # factory
    factory = BribesFactory.deploy({"from": token_whale})
    # this will show the gas cost of deploying the BribesManager contract using the factory contract
    manager_f = factory.deployManager(
        TOKEN, GAUGE_INDEX, TOKENS_PER_VOTE, {"from": token_whale})
