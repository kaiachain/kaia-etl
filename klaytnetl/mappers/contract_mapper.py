# MIT License
#
# Modifications Copyright (c) klaytn authors
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from klaytnetl.domain.contract import KlaytnRawContract, KlaytnContract
from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin

from typing import Union


class KlaytnContractMapper(BaseMapper, EnrichableMixin):
    def __init__(self, enrich: bool = False):
        super(KlaytnContractMapper, self).__init__(enrich=enrich)

    # FIXME
    def rpc_result_to_contract(
        self, contract_address, rpc_result
    ) -> Union[KlaytnRawContract, KlaytnContract]:
        contract = KlaytnRawContract()
        contract.address = contract_address
        contract.bytecode = rpc_result

        return contract

    def contract_to_dict(
        self, contract: Union[KlaytnRawContract, KlaytnContract], serializable=True
    ) -> dict:
        contract_dict: dict = {
            "type": "contract",
            "address": contract.address,
            "bytecode": contract.bytecode,
            "function_sighashes": contract.function_sighashes,
            "is_erc20": contract.is_erc20,
            "is_erc721": contract.is_erc721,
            "block_number": contract.block_number,
        }

        if self.enrich and isinstance(contract, KlaytnContract):
            contract_dict["block_hash"] = contract.block_hash
            contract_dict["block_unix_timestamp"] = contract.block_timestamp.timestamp()
            contract_dict["block_timestamp"] = (
                contract.block_timestamp.isoformat()
                if serializable
                else contract.block_timestamp
            )
            contract_dict["transaction_hash"] = contract.transaction_hash
            contract_dict["transaction_index"] = contract.transaction_index
            contract_dict[
                "transaction_receipt_status"
            ] = contract.transaction_receipt_status
            contract_dict["trace_index"] = contract.trace_index
            contract_dict["trace_status"] = contract.trace_status
            contract_dict["creator_address"] = contract.creator_address

        return contract_dict
