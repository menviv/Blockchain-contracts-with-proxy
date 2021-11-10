from brownie import Box, network, Contract, ProxyAdmin, TransparentUpgradeableProxy, BoxV2
from scripts.helpful_scripts import get_account, encode_function_data, upgrade

def test_proxy_delegate_calls():
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

    
    
