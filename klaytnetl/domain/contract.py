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


from klaytnetl.domain.base import BaseDomain
from klaytnetl.domain.trace import KlaytnRawTrace, KlaytnTrace
from klaytnetl.service.klaytn_contract_service import KlaytnContractService
from klaytnetl.utils import float_to_datetime, validate_address, type_conversion
from datetime import datetime
from typing import Union


class KlaytnRawContract(BaseDomain):
    def __init__(self):
        self._address: str = None
        self._bytecode: str = None
        self._function_sighashes: list = []
        self._is_erc20: bool = False
        self._is_erc721: bool = False
        self._is_erc1155: bool = False
        self._block_number: int = None

    ### Prop: address ###
    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = validate_address(value, digits=42)

    @address.deleter
    def address(self) -> None:
        del self._address

    ### Prop: bytecode ###
    @property
    def bytecode(self) -> str:
        return self._bytecode

    @bytecode.setter
    def bytecode(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmached: contract.bytecode must be {str}.")

        self._bytecode = value

    @bytecode.deleter
    def bytecode(self) -> None:
        del self._bytecode

    ### Prop: function_sighashes ###
    @property
    def function_sighashes(self) -> list:
        return self._function_sighashes

    @function_sighashes.setter
    def function_sighashes(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(
                f"TypeUnmached: contract.function_sighashes must be {list}."
            )

        self._function_sighashes = value

    @function_sighashes.deleter
    def function_sighashes(self) -> None:
        del self._function_sighashes

    ### Prop: is_erc20 ###
    @property
    def is_erc20(self) -> bool:
        return self._is_erc20

    @is_erc20.setter
    def is_erc20(self, value: bool) -> None:
        value = type_conversion("contract.is_erc20", value, bool)
        self._is_erc20 = value

    @is_erc20.deleter
    def is_erc20(self) -> None:
        del self._is_erc20

    ### Prop: is_erc721 ###
    @property
    def is_erc721(self) -> bool:
        return self._is_erc721

    @is_erc721.setter
    def is_erc721(self, value: bool) -> None:
        value = type_conversion("contract.is_erc721", value, bool)
        self._is_erc721 = value

    @is_erc721.deleter
    def is_erc721(self) -> None:
        del self._is_erc721

    ### Prop: is_erc1155 ###
    @property
    def is_erc1155(self) -> bool:
        return self._is_erc1155

    @is_erc1155.setter
    def is_erc1155(self, value: bool) -> None:
        value = type_conversion("contract.is_erc1155", value, bool)
        self._is_erc1155 = value

    @is_erc1155.deleter
    def is_erc1155(self) -> None:
        del self._is_erc1155

    ### Prop: block_number ###
    @property
    def block_number(self) -> int:
        return self._block_number

    @block_number.setter
    def block_number(self, value: int) -> None:
        value = type_conversion("contract.block_number", value, int)
        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

    @staticmethod
    def from_trace(
        trace: Union[KlaytnRawTrace, KlaytnTrace],
        contract_service: KlaytnContractService,
    ):
        contract = KlaytnRawContract()

        if trace.to_address is None:
            raise ValueError(
                "ValueNotAllowed: contract creation trace must have to_address."
            )
        else:
            contract.address = trace.to_address
        contract.bytecode = trace.output
        contract.function_sighashes = contract_service.get_function_sighashes(
            contract.bytecode
        )

        contract.is_erc20 = contract_service.is_erc20_contract(
            contract.function_sighashes
        )
        contract.is_erc721 = contract_service.is_erc721_contract(
            contract.function_sighashes
        )
        contract.block_number = trace.block_number

        return contract


class KlaytnContract(KlaytnRawContract):
    def __init__(self):
        super(KlaytnContract, self).__init__()

        self._block_hash: str = None
        self._block_timestamp: datetime = None
        self._transaction_hash: str = None
        self._transaction_index: int = None
        self._transaction_receipt_status: int = None
        self._trace_index: int = None
        self._trace_status: int = None
        self._creator_address: str = None  # contract creator address

    ### Prop: block_hash ###
    @property
    def block_hash(self) -> str:
        return self._block_hash

    @block_hash.setter
    def block_hash(self, value: str) -> None:
        self._block_hash = validate_address(value, digits=66)

    @block_hash.deleter
    def block_hash(self) -> None:
        del self._block_hash

    ### Prop: block_timestamp ###
    @property
    def block_timestamp(self) -> datetime:
        return self._block_timestamp

    @block_timestamp.setter
    def block_timestamp(self, value: Union[datetime, float, int]) -> None:
        self._block_timestamp = float_to_datetime(value)

    @block_timestamp.deleter
    def block_timestamp(self) -> None:
        del self._block_timestamp

    ### Prop: transaction_hash ###
    @property
    def transaction_hash(self) -> str:
        return self._transaction_hash

    @transaction_hash.setter
    def transaction_hash(self, value: str) -> None:
        self._transaction_hash = validate_address(value, digits=66)

    @transaction_hash.deleter
    def transaction_hash(self) -> None:
        del self._transaction_hash

    ### Prop: transaction_index ###
    @property
    def transaction_index(self) -> int:
        return self._transaction_index

    @transaction_index.setter
    def transaction_index(self, value: int) -> None:
        value = type_conversion("contract.transaction_index", value, int)
        self._transaction_index = value

    @transaction_index.deleter
    def transaction_index(self) -> None:
        del self._transaction_index

    ### Prop: transaction_receipt_status ###
    @property
    def transaction_receipt_status(self) -> int:
        return self._transaction_receipt_status

    @transaction_receipt_status.setter
    def transaction_receipt_status(self, value: int) -> None:
        value = type_conversion("contract.transaction_receipt_status", value, int)
        self._transaction_receipt_status = value

    @transaction_receipt_status.deleter
    def transaction_receipt_status(self) -> None:
        del self._transaction_receipt_status

    ### Prop: trace_index ###
    @property
    def trace_index(self) -> int:
        return self._trace_index

    @trace_index.setter
    def trace_index(self, value: int) -> None:
        value = type_conversion("contract.trace_index", value, int)
        self._trace_index = value

    @trace_index.deleter
    def trace_index(self) -> None:
        del self._trace_index

    ### Prop: trace_status ###
    @property
    def trace_status(self) -> int:
        return self._trace_status

    @trace_status.setter
    def trace_status(self, value: int) -> None:
        value = type_conversion("contract.trace_status", value, int)
        self._trace_status = value

    @trace_status.deleter
    def trace_status(self) -> None:
        del self._trace_status

    ### Prop: creator_address ###
    @property
    def creator_address(self) -> str:
        return self._creator_address

    @creator_address.setter
    def creator_address(self, value: str) -> None:
        self._creator_address = validate_address(value, digits=42)

    @creator_address.deleter
    def creator_address(self) -> None:
        del self._creator_address

    @staticmethod
    def enrich(
        raw_contract: KlaytnRawContract,
        block_timestamp,
        block_hash,
        transaction_hash,
        transaction_index,
        transaction_receipt_status,
        trace_index,
        trace_status,
        creator_address,
    ):
        contract = KlaytnContract()

        for k, v in raw_contract.__dict__.items():
            if hasattr(contract, k):
                contract.__setattr__(k, v)

        # block
        contract.block_hash = block_hash
        contract.block_timestamp = block_timestamp

        # transaction
        contract.transaction_hash = transaction_hash
        contract.transaction_index = transaction_index
        contract.transaction_receipt_status = transaction_receipt_status

        # trace
        contract.trace_index = trace_index
        contract.trace_status = trace_status
        contract.creator_address = creator_address

        return contract

    @staticmethod
    def from_trace(
        trace: Union[KlaytnRawTrace, KlaytnTrace],
        contract_service: KlaytnContractService,
    ):
        if not isinstance(trace, KlaytnTrace):
            raise TypeError(
                f"ParameterTypeError: Cannot create {KlaytnContract} from {KlaytnRawTrace}. Use {KlaytnTrace}, instead."
            )
        else:
            raw_contract: KlaytnRawContract = KlaytnRawContract.from_trace(
                trace, contract_service
            )

            return KlaytnContract.enrich(
                raw_contract,
                block_hash=trace.block_hash,
                block_timestamp=trace.block_timestamp,
                transaction_hash=trace.transaction_hash,
                transaction_index=trace.transaction_index,
                transaction_receipt_status=trace.transaction_receipt_status,
                trace_index=trace.trace_index,
                trace_status=trace.status,
                creator_address=trace.from_address,
            )
