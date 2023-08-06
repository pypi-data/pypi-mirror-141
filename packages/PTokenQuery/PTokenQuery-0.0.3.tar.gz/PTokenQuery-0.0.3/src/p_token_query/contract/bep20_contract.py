from p_token_query.config import GlobalInfoConfig


class Bep20Contract:
    def __init__(self, web3, token_address):
        self.web3 = web3
        self.address = token_address
        self._contract = web3.eth.contract(address=token_address, abi=GlobalInfoConfig.AbiConfig.BEP20_ABI)

    def get_decimal(self):
        return self._contract.functions.decimals().call()

    def get_name(self):
        return self._contract.functions.name().call()

    def get_symbol(self):
        return self._contract.functions.symbol().call()

    def get_owner(self):
        return self._contract.functions.getOwner().call()

    def get_balance(self, account_address, block_identifier=None):
        if block_identifier is not None:
            return self._contract.functions.balanceOf(account_address).call(block_identifier=block_identifier)
        return self._contract.functions.balanceOf(account_address).call()
