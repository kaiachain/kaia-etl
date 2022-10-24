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
from klaytnetl.domain.contract import KlaytnRawContract, KlaytnContract
from klaytnetl.utils import (
    int_to_decimal,
    float_to_datetime,
    validate_address,
    type_conversion,
)
from datetime import datetime
from decimal import Decimal
from typing import Union, Optional


class KlaytnRawToken(BaseDomain):
    def __init__(self):
        self._address: str = None
        self._symbol: Optional[str] = None
        self._name: Optional[str] = None
        self._decimals: Optional[int] = None
        self._total_supply: Union[int, Decimal, None] = None
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

    ### Prop: symbol ###
    @property
    def symbol(self) -> Optional[str]:
        return self._symbol

    @symbol.setter
    def symbol(self, value: Optional[str]) -> None:
        if value is None:
            self._symbol = None
        elif not isinstance(value, str):
            raise TypeError(f"TypeUnmached: token.symbol must be {Optional[str]}.")
        else:
            self._symbol = value

    @symbol.deleter
    def symbol(self) -> None:
        del self._symbol

    ### Prop: name ###
    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is None:
            self._name = None
        elif not isinstance(value, str):
            raise TypeError(f"TypeUnmached: token.name must be {Optional[str]}.")
        else:
            self._name = value

    @name.deleter
    def name(self) -> None:
        del self._name

    ### Prop: decimals ###
    @property
    def decimals(self) -> Optional[int]:
        return self._decimals

    @decimals.setter
    def decimals(self, value: Optional[int]) -> None:
        if value is None:
            self._decimals = None
        else:
            value = type_conversion("token.decimals", value, int)
            self._decimals = value

    @decimals.deleter
    def decimals(self) -> None:
        del self._decimals

    ### Prop: total_supply ###
    @property
    def total_supply(self) -> Union[int, Decimal, None]:
        return self._total_supply

    @total_supply.setter
    def total_supply(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            self._total_supply = None
        else:
            self._total_supply = int_to_decimal(value)

    @total_supply.deleter
    def total_supply(self) -> None:
        del self._total_supply

    ### Prop: block_number ###
    @property
    def block_number(self) -> int:
        return self._block_number

    @block_number.setter
    def block_number(self, value: int) -> None:
        value = type_conversion("token.block_number", value, int)
        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

    @staticmethod
    def from_contract(
        contract: Union[KlaytnRawContract, KlaytnContract],
        symbol=None,
        name=None,
        decimals=None,
        total_supply=None,
    ):
        token = KlaytnRawToken()

        for k, v in contract.__dict__.items():
            if hasattr(token, k):
                token.__setattr__(k, v)

        token.symbol = symbol
        token.name = name
        token.decimals = decimals
        token.total_supply = total_supply

        return token


class KlaytnToken(KlaytnRawToken):
    def __init__(self):
        super(KlaytnToken, self).__init__()

        self._function_sighashes: list = None
        self._is_erc20: bool = None
        self._is_erc721: bool = None
        self._is_erc1155: bool = None
        self._block_hash: str = None
        self._block_timestamp: datetime = None
        self._transaction_hash: str = None
        self._transaction_index: int = None
        self._transaction_receipt_status: int = None
        self._trace_index: int = None
        self._trace_status: int = None
        self._creator_address: str = None

    ### Prop: function_sighashes ###
    @property
    def function_sighashes(self) -> list:
        return self._function_sighashes

    @function_sighashes.setter
    def function_sighashes(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmached: token.function_sighashes must be {list}.")

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
        value = type_conversion("token.is_erc20", value, bool)
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
        value = type_conversion("token.is_erc721", value, bool)
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
        value = type_conversion("token.is_erc1155", value, bool)
        self._is_erc1155 = value

    @is_erc1155.deleter
    def is_erc1155(self) -> None:
        del self._is_erc1155

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
        value = type_conversion("token.transaction_index", value, int)
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
        value = type_conversion("token.transaction_receipt_status", value, int)
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
        value = type_conversion("token.trace_index", value, int)
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
        value = type_conversion("token.trace_status", value, int)
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
        raw_token: KlaytnRawToken,
        function_sighashes,
        is_erc20,
        is_erc721,
        is_erc1155,
        block_hash,
        block_timestamp,
        transaction_hash,
        transaction_index,
        transaction_receipt_status,
        trace_index,
        trace_status,
        creator_address,
    ):
        token = KlaytnToken()

        for k, v in raw_token.__dict__.items():
            if hasattr(token, k):
                token.__setattr__(k, v)

        # contract
        token.function_sighashes = function_sighashes
        token.is_erc20 = is_erc20
        token.is_erc721 = is_erc721
        token.is_erc1155 = is_erc1155

        # block
        token.block_hash = block_hash
        token.block_timestamp = block_timestamp

        # transaction
        token.transaction_hash = transaction_hash
        token.transaction_index = transaction_index
        token.transaction_receipt_status = transaction_receipt_status

        # trace
        token.trace_index = trace_index
        token.trace_status = trace_status
        token.creator_address = creator_address

        return token

    @staticmethod
    def from_contract(
        contract: Union[KlaytnRawContract, KlaytnContract],
        symbol=None,
        name=None,
        decimals=None,
        total_supply=None,
    ):
        if not isinstance(contract, KlaytnContract):
            raise TypeError(
                f"ParameterTypeError: Cannot create {KlaytnToken} from {KlaytnRawContract}. "
                f"Use {KlaytnContract}, instead."
            )
        else:
            raw_token: KlaytnRawToken = KlaytnRawToken.from_contract(
                contract,
                symbol=symbol,
                name=name,
                decimals=decimals,
                total_supply=total_supply,
            )

            return KlaytnToken.enrich(
                raw_token,
                function_sighashes=contract.function_sighashes,
                is_erc20=contract.is_erc20,
                is_erc721=contract.is_erc721,
                is_erc1155=contract.is_erc1155,
                block_hash=contract.block_hash,
                block_timestamp=contract.block_timestamp,
                transaction_hash=contract.transaction_hash,
                transaction_index=contract.transaction_index,
                transaction_receipt_status=contract.transaction_receipt_status,
                trace_index=contract.trace_index,
                trace_status=contract.trace_status,
                creator_address=contract.creator_address,
            )
