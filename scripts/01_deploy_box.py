from brownie import Box, network, Contract, ProxyAdmin, TransparentUpgradeableProxy, BoxV2
from scripts.helpful_scripts import get_account, encode_function_data, upgrade

def main():
    account=get_account()
    print(f"Deploying to {network.show_active()}")
    # This is an implementation conytract
    box = Box.deploy({"from": account})
    print(f"Retrieve from Box contract {box.retrieve()}")

    proxy_admin = ProxyAdmin.deploy({"from": account})

    #initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit" : 1000000},
    )
    print(f"Proxy deployed to  {proxy}, you can now upgrade to V2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(3, {"from": account})
    print(f"Retrieve from Proxy Box {proxy_box.retrieve()}")

    box_v2 = BoxV2.deploy({"from": account})
    print(f"Retrieve from Box2 contract {box_v2.retrieve()}")
    upgrade_tx = upgrade(account, proxy, box_v2.address, proxy_admin_contract = proxy_admin)
    print("Proxy has been upgraded!")

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.imncrememnt({"from": account})
    print(f"Retrieve from Proxy Box2 {proxy_box.retrieve()}")


    