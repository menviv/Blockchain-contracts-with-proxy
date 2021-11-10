from brownie import Box, network, Contract, ProxyAdmin, TransparentUpgradeableProxy, BoxV2, exceptions
from scripts.helpful_scripts import get_account, encode_function_data, upgrade
import pytest

def test_proxy_upgards():
    account = get_account()
    box = Box.deploy({"from":account})
    proxy_admin = ProxyAdmin.deploy({"from":account})
    box_encoded_initiliazer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initiliazer_function,
        {"from": account, "gas_limit": 1000000}
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1

    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.imncrememnt({"from": account})

    upgrade_tx = upgrade(account, proxy, box_v2.address, proxy_admin_contract = proxy_admin)

    proxy_box.imncrememnt({"from": account})
    assert proxy_box.retrieve() == 2