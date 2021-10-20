"""
Utils for connecting to an EVM contract
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import web3
from eth_typing.evm import ChecksumAddress
from telliot.model.endpoints import RPCEndpoint
from telliot.utils.base import Base
from telliot.utils.response import ContractResponse
from web3 import Web3


class Contract(Base):
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    #: Contract address
    address: Union[str, ChecksumAddress]

    #: ABI specifications of contract
    abi: Union[List[Dict[str, Any]], str]

    #: web3 contract object
    contract: Optional[web3.contract.Contract]

    #: global pytelliot configurations
    # config: ConfigOptions

    def connect(self) -> ContractResponse:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3 is None:
            msg = "node is not instantiated"
            return ContractResponse(ok=False, error_msg=msg)
        else:
            if not self.node.connect():
                msg = "node is not connected"
                return ContractResponse(ok=False, error_msg=msg, endpoint=self.node)
            self.address = Web3.toChecksumAddress(self.address)
            self.contract = self.node.web3.eth.contract(
                address=self.address, abi=self.abi
            )
            return ContractResponse(ok=True, endpoint=self.node)

    def read(self, func_name: str, **kwargs: Any) -> ContractResponse:
        """
        Reads data from contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        ContractResponse: standard response for contract data
        """

        if self.contract:
            try:
                contract_function = self.contract.get_function_by_name(func_name)
                output = contract_function(**kwargs).call()
                return ContractResponse(ok=True, result=output)
            except ValueError as e:
                msg = f"function '{func_name}' not found in contract abi"
                return ContractResponse(
                    ok=False, error=e, error_msg=msg, endpoint=self.node
                )
        else:
            if self.connect():
                msg = "now connected to contract"
                return self.read(func_name=func_name, **kwargs)
            else:
                msg = "unable to connect to contract"
                return ContractResponse(ok=False, error_msg=msg, endpoint=self.node)

    # def write(self, func_name: str, **kwargs: Any) -> bool:
    #     """
    #     Writes data to contract
    #     inputs:
    #     func_name (str): name of contract function to call

    #     returns:
    #     bool: success
    #     """
    #     try:
    #         # load account from private key
    #         self.acc = self.node.web3.eth.account.from_key(self.config.private_key)
    #         # get account nonce
    #         acc_nonce = self.node.web3.eth.get_transaction_count(self.acc.address)
    #         # get fast gas price
    #         req = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    #         prices = json.loads(req.content)
    #         gas_price = str(prices["fast"])
    #         print("retrieved gas price:", gas_price)
    #         # find function in contract
    #         contract_function = self.contract.get_function_by_name(func_name)
    #         tx = contract_function(**kwargs)
    #         # estimate gas
    #         estimated_gas = tx.estimateGas()
    #         # build transaction
    #         tx_built = tx.build_transaction(
    #             {
    #                 "nonce": acc_nonce,
    #                 "gas": estimated_gas,
    #                 "gasPrice": self.node.web3.toWei(gas_price, "gwei"),
    #                 "chainId": self.config.chain_id,
    #             }
    #         )

    #         tx_signed = self.acc.sign_transaction(tx_built)

    #         tx_hash = self.node.web3.eth.send_raw_transaction(tx_signed.rawTransaction)
    #         print(
    #             f"View reported data: https://rinkeby.etherscan.io/tx/{tx_hash.hex()}"
    #         )

    #         _ = self.node.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=360)

    #         return True
    #     except Exception:
    #         print("tx was unsuccessful")
    #         return False

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
