from brownie import network, accounts, config
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
        print("index: ", index)
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


#initializer=box.store, 1, 2, 3, 4...
def encode_function_data(initializer=None, *args):
    if len(args)==0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)

def upgrade(account, proxy, new_implementaion_address, proxy_admin_contract=None, initializer=None, *args):
    transaction=None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementaion_address,
                encode_function_call,
                {"from": account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address,
                new_implementaion_address,
                {"from": account}
            )
    else:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeAndCall(
                new_implementaion_address,
                encode_function_call,
                {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(
                new_implementaion_address,
                {"from": account}
            ) 

