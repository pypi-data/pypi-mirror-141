import json
from web3 import Web3
from p_token_query.contract.bep20_contract import Bep20Contract


class Bep20Query:
    def __init__(self, web3, file_path=None):
        self._web3 = web3
        self._file_path = file_path
        if file_path is None:
            self._file_data = {}
        else:
            self._file_data = json.loads(open(file_path, 'r').read())

    def get_token_config(self, token_address: str):
        low_token_address = token_address.lower()
        if low_token_address in self._file_data:
            return self._file_data[low_token_address]
        else:
            try:
                bep20_contract = Bep20Contract(self._web3, Web3.toChecksumAddress(token_address))
                _decimal = bep20_contract.get_decimal()
                _name = bep20_contract.get_name()
                _symbol = bep20_contract.get_symbol()
                result = {
                    "code": _symbol,
                    "name": _name,
                    "decimal": _decimal,
                    "address": low_token_address,
                }
                self._file_data[low_token_address] = result
                if self._file_path is not None:
                    write_state = open(self._file_path, "w")
                    json.dump(self._file_data, write_state, ensure_ascii=False)
                    write_state.close()
                return result
            except Exception as error:
                print(error)
                return None
