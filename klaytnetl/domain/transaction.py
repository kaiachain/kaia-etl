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
from klaytnetl.utils import (
    int_to_decimal,
    float_to_datetime,
    validate_address,
    type_conversion,
)
from datetime import datetime
from decimal import Decimal
from typing import Union, Optional


class KlaytnRawTransaction(BaseDomain):
    def __init__(self):
        self._hash: str = None
        self._nonce: int = None
        self._block_hash: str = None
        self._block_number: int = None
        self._transaction_index: int = None
        self._from_address: str = None
        self._to_address: Optional[str] = None
        self._value: Union[None, int, Decimal] = None
        self._gas: Union[int, Decimal, None] = None
        self._gas_price: Union[int, Decimal, None] = None
        self._input: Optional[str] = None

        self._logs: list = []

        self._fee_payer: Optional[
            str
        ] = None  # (Optional) Data: 20 byte, address of the fee payer.
        self._fee_payer_signatures: Optional[
            list
        ] = []  # (Optional) Array: An array of fee payer's signature objects.
        # A signature object contains three fields (V, R, and S).
        self._fee_ratio: Optional[int] = 0  # (Optional) Fee ratio of the fee payer.
        # If it is 30, 30% of the fee will be paid by the fee payer.

        self._sender_tx_hash: str = None  # Data: 32 byte, Hash of the tx without the fee payer's address and signature.
        self._signatures: list = []  # Array: An array of signature objects.
        # A signature object contains three fields (V, R, and S).

        self._tx_type: str = (
            None  # String: A string representing the type of the transaction.
        )
        self._tx_type_int: int = (
            None  # Quantity: An integer representing the type of the transaction.
        )

        self._max_priority_fee_per_gas: Union[int, Decimal, None] = None
        self._max_fee_per_gas: Union[int, Decimal, None] = None
        self._access_list: Optional[list] = []

    ### Prop: hash ###
    @property
    def hash(self) -> str:
        return self._hash

    @hash.setter
    def hash(self, value: str) -> None:
        self._hash = validate_address(value, digits=66)

    @hash.deleter
    def hash(self) -> None:
        del self._hash

    ### Prop: nonce ###
    @property
    def nonce(self) -> int:
        return self._nonce

    @nonce.setter
    def nonce(self, value) -> None:
        value = type_conversion("transaction.nonce", value, int)
        self._nonce = value

    @nonce.deleter
    def nonce(self) -> None:
        del self._nonce

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

    ### Prop: block_number ###
    @property
    def block_number(self) -> int:
        return self._block_number

    @block_number.setter
    def block_number(self, value: int) -> None:
        value = type_conversion("transaction.block_number", value, int)
        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

    ### Prop: transaction_index ###
    @property
    def transaction_index(self) -> int:
        return self._transaction_index

    @transaction_index.setter
    def transaction_index(self, value: int) -> None:
        value = type_conversion("transaction.transaction_index", value, int)
        self._transaction_index = value

    @transaction_index.deleter
    def transaction_index(self) -> None:
        del self._transaction_index

    ### Prop: from_address ###
    @property
    def from_address(self) -> str:
        return self._from_address

    @from_address.setter
    def from_address(self, value: str) -> None:
        if value is None:
            raise TypeError(
                f"TypeUnmatched: transaction.from_address cannot be {None}."
            )
        else:
            self._from_address = validate_address(value)

    @from_address.deleter
    def from_address(self) -> None:
        del self._from_address

    ### Prop: to_address ###
    @property
    def to_address(self) -> Optional[str]:
        return self._to_address

    @to_address.setter
    def to_address(self, value: Optional[str]) -> None:
        self._to_address = validate_address(value) if value is not None else None

    @to_address.deleter
    def to_address(self) -> None:
        del self._to_address

    ### Prop: value ###
    @property
    def value(self) -> Union[None, int, Decimal]:
        return self._value

    @value.setter
    def value(self, value: Union[None, int, Decimal]) -> None:
        if value is None:
            self._value = 0
        else:
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: transaction.value must be a non-negative decimal."
                )
            self._value = value

    @value.deleter
    def value(self) -> None:
        del self._value

    ### Prop: gas ###
    @property
    def gas(self) -> Union[int, Decimal, None]:
        return self._gas

    @gas.setter
    def gas(self, value: Union[int, Decimal, None]) -> None:
        value = int_to_decimal(value)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: transaction.gas must be a non-negative decimal."
            )
        self._gas = value

    @gas.deleter
    def gas(self) -> None:
        del self._gas

    ### Prop: gas_price ###
    @property
    def gas_price(self) -> Union[int, Decimal, None]:
        return self._gas_price

    @gas_price.setter
    def gas_price(self, value: Union[None, int, Decimal]) -> None:
        value = int_to_decimal(value)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: transaction.gas_price must be a non-negative decimal."
            )

        self._gas_price = value

    @gas_price.deleter
    def gas_price(self) -> None:
        del self._gas_price

    ### Prop: input ###
    @property
    def input(self) -> Union[str, None]:
        return self._input

    @input.setter
    def input(self, value: Union[str, None]) -> None:
        if value is not None and not isinstance(value, str):
            raise TypeError(
                f"TypeUnmatched: transaction.input must be {Union[str, None]}."
            )

        self._input = value

    @input.deleter
    def input(self) -> None:
        del self._input

    ### Prop: logs ###
    @property
    def logs(self) -> list:
        return self._logs

    @logs.setter
    def logs(self, value) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: transaction.logs must be {list}.")

        self._logs = value

    @logs.deleter
    def logs(self) -> None:
        del self._logs

    ### Prop: fee_payer ###
    @property
    def fee_payer(self) -> Optional[str]:
        return self._fee_payer

    @fee_payer.setter
    def fee_payer(self, value: Optional[str]) -> None:
        self._fee_payer = validate_address(value) if value is not None else None

    @fee_payer.deleter
    def fee_payer(self) -> None:
        del self._fee_payer

    ### Prop: fee_payer_signatures ###
    @property
    def fee_payer_signatures(self) -> list:
        return (
            self._fee_payer_signatures if self._fee_payer_signatures is not None else []
        )

    @fee_payer_signatures.setter
    def fee_payer_signatures(self, value: Optional[list]) -> None:
        if value is not None and not isinstance(value, list):
            raise TypeError(
                f"TypeUnmatched: transaction.fee_payer_signatures must be {Optional[list]}."
            )

        self._fee_payer_signatures = value

    @fee_payer_signatures.deleter
    def fee_payer_signatures(self) -> None:
        del self._fee_payer_signatures

    ### Prop: fee_ratio ###
    @property
    def fee_ratio(self) -> int:
        if self._fee_payer is None:
            return 0
        else:
            return 100 if self._fee_ratio is None else self._fee_ratio

    @fee_ratio.setter
    def fee_ratio(self, value: Optional[int]) -> None:
        if value is None:
            self._fee_ratio = None
        else:
            value = type_conversion("transaction.fee_ratio", value, int)
            if value < 0 or value > 100:
                raise ValueError(
                    "ValueNotAllowed: transaction.fee_ratio must be an integer between 0 and 100, "
                    "inclusively."
                )
            else:
                self._fee_ratio = value

    @fee_ratio.deleter
    def fee_ratio(self) -> None:
        del self._fee_ratio

    ### Prop: sender_tx_hash ###
    @property
    def sender_tx_hash(self) -> str:
        return self._sender_tx_hash

    @sender_tx_hash.setter
    def sender_tx_hash(self, value: str) -> None:
        self._sender_tx_hash = validate_address(value, digits=66)

    @sender_tx_hash.deleter
    def sender_tx_hash(self) -> None:
        del self._sender_tx_hash

    ### Prop: signatures ###
    @property
    def signatures(self) -> list:
        return self._signatures

    @signatures.setter
    def signatures(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: transaction.signatures must be {list}.")

        self._signatures = value

    @signatures.deleter
    def signatures(self) -> None:
        del self._signatures

    ### Prop: tx_type ###
    @property
    def tx_type(self) -> str:
        return self._tx_type

    @tx_type.setter
    def tx_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: transaction.tx_type must be {str}.")

        self._tx_type = value

    @tx_type.deleter
    def tx_type(self) -> None:
        del self._tx_type

    ### Prop: tx_type_int ###
    @property
    def tx_type_int(self) -> int:
        return self._tx_type_int

    @tx_type_int.setter
    def tx_type_int(self, value: int) -> None:
        value = type_conversion("transaction.tx_type_int", value, int)
        self._tx_type_int = value

    @tx_type_int.deleter
    def tx_type_int(self) -> None:
        del self._tx_type_int

    ### Prop: max_priority_fee_per_gas ###
    @property
    def max_priority_fee_per_gas(self) -> Union[int, Decimal, None]:
        return self._max_priority_fee_per_gas

    @max_priority_fee_per_gas.setter
    def max_priority_fee_per_gas(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            self._max_priority_fee_per_gas = None
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: transaction.max_priority_fee_per_gas"
                    " must be a non-negative decimal."
                )
            self._max_priority_fee_per_gas = value

    @max_priority_fee_per_gas.deleter
    def max_priority_fee_per_gas(self) -> None:
        del self._max_priority_fee_per_gas

    ### Prop: max_fee_per_gas ###
    @property
    def max_fee_per_gas(self) -> Union[int, Decimal, None]:
        return self._max_fee_per_gas

    @max_fee_per_gas.setter
    def max_fee_per_gas(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            self._max_priority_fee_per_gas = None
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: transaction.max_fee_per_gas must be a non-negative decimal."
                )
            self._max_fee_per_gas = value

    @max_fee_per_gas.deleter
    def max_fee_per_gas(self) -> None:
        del self._max_fee_per_gas

    ### Prop: access_list ###
    @property
    def access_list(self) -> list:
        return self._access_list if self._access_list is not None else []

    @access_list.setter
    def access_list(self, value: Optional[list]) -> None:
        if value is not None and not isinstance(value, list):
            raise TypeError(
                f"TypeUnmatched: transaction.signatures must be {Optional[list]}."
            )
        self._access_list = value

    @access_list.deleter
    def access_list(self) -> None:
        del self._access_list


class KlaytnTransaction(KlaytnRawTransaction):
    def __init__(self):
        super(KlaytnTransaction, self).__init__()

        self._block_timestamp: datetime = None  # block timestamp
        self._receipt_gas_used: Union[
            int, Decimal, None
        ] = None  # gas used to execute the transaction
        self._receipt_contract_address: Optional[str] = None  # created contact
        self._receipt_status: int = None  # receipt status

    ### Prop: to_address ###
    @property
    def to_address(self) -> Optional[str]:
        return (
            self._to_address
            if self._to_address is not None
            else self._receipt_contract_address
        )

    @to_address.setter
    def to_address(self, value: Optional[str]) -> None:
        self._to_address = (
            validate_address(value, digits=42) if value is not None else None
        )

    @to_address.deleter
    def to_address(self) -> None:
        del self._to_address

    ### Prop: block_timestamp ###
    @property
    def block_timestamp(self) -> datetime:
        return self._block_timestamp

    @block_timestamp.setter
    def block_timestamp(self, value: Union[datetime, float, int]) -> None:
        self._block_timestamp = float_to_datetime(value)

    @block_timestamp.deleter
    def block_timestamp(self) -> None:
        self._block_timestamp

    ### Prop: receipt_gas_used ###
    @property
    def receipt_gas_used(self) -> Union[int, Decimal, None]:
        return self._receipt_gas_used

    @receipt_gas_used.setter
    def receipt_gas_used(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            value = 0
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: transaction.receipt_gas_used must be a non-negative decimal."
                )

        self._receipt_gas_used = value

    @receipt_gas_used.deleter
    def receipt_gas_used(self) -> None:
        del self._receipt_gas_used

    ### Prop: receipt_contract_address ###
    @property
    def receipt_contract_address(self) -> Optional[str]:
        return self._receipt_contract_address

    @receipt_contract_address.setter
    def receipt_contract_address(self, value: Optional[str]) -> None:
        self._receipt_contract_address = (
            validate_address(value, digits=42) if value is not None else None
        )

    @receipt_contract_address.deleter
    def receipt_contract_address(self) -> None:
        del self._receipt_contract_address

    ### Prop: receipt_status ###
    @property
    def receipt_status(self) -> int:
        return self._receipt_status

    @receipt_status.setter
    def receipt_status(self, value: int) -> None:
        value = type_conversion("transaction.receipt_status", value, int)
        self._receipt_status = value

    @receipt_status.deleter
    def receipt_status(self) -> None:
        del self._receipt_status

    @staticmethod
    def enrich(
        raw_transaction: KlaytnRawTransaction,
        block_timestamp,
        receipt_gas_used,
        receipt_contract_address,
        receipt_status,
    ):
        transaction = KlaytnTransaction()

        for k, v in raw_transaction.__dict__.items():
            if hasattr(transaction, k):
                transaction.__setattr__(k, v)

        # timestamps
        transaction.block_timestamp = block_timestamp

        # receipt info
        transaction.receipt_gas_used = receipt_gas_used
        transaction.receipt_contract_address = receipt_contract_address
        transaction.receipt_status = receipt_status

        # missing to address
        # transaction.to_address = raw_transaction.to_address if raw_transaction.to_address is not None else receipt_contract_address

        return transaction
