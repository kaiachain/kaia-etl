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
    float_to_datetime,
    validate_address,
    type_conversion
)
from datetime import datetime
from decimal import Decimal
from typing import Union


class KlaytnRawTokenTransfer(BaseDomain):
    def __init__(self):
        self._token_address: str = None
        self._from_address: str = None
        self._to_address: str = None
        self._value: Union[None, int, Decimal] = None
        self._log_index: int = None
        self._transaction_hash: str = None
        self._transaction_index: int = None
        self._block_hash: str = None
        self._block_number: int = None

    ### Prop: token_address ###
    @property
    def token_address(self) -> str:
        return self._token_address

    @token_address.setter
    def token_address(self, value: str) -> None:
        self._token_address = validate_address(value)

    @token_address.deleter
    def token_address(self) -> None:
        del self._token_address

    ### Prop: from_address ###
    @property
    def from_address(self) -> str:
        return self._from_address

    @from_address.setter
    def from_address(self, value: str) -> None:
        self._from_address = validate_address(value)

    @from_address.deleter
    def from_address(self) -> None:
        del self._from_address

    ### Prop: to_address ###
    @property
    def to_address(self) -> str:
        return self._to_address

    @to_address.setter
    def to_address(self, value: str) -> None:
        self._to_address = validate_address(value)

    @to_address.deleter
    def to_address(self) -> None:
        del self._to_address

    ### Prop: value ###
    @property
    def value(self) -> Decimal:
        return self._value

    @value.setter
    def value(self, value: Union[None, int, Decimal]) -> None:
        if value is None:
            self._value = 0
        else:
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: token_transfer.value must be a non-negative decimal."
                )
            self._value = value

    @value.deleter
    def value(self) -> None:
        del self._value

    ### Prop: log_index ###
    @property
    def log_index(self) -> int:
        return self._log_index

    @log_index.setter
    def log_index(self, value: int) -> None:
        value = type_conversion("log_index", value, int)
        self._log_index = value

    @log_index.deleter
    def log_index(self) -> None:
        del self._log_index

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
        value = type_conversion("transaction_index", value, int)
        self._transaction_index = value

    @transaction_index.deleter
    def transaction_index(self) -> None:
        del self._transaction_index

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
        value = type_conversion("block_number", value, int)
        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number


class KlaytnTokenTransfer(KlaytnRawTokenTransfer):
    def __init__(self):
        super(KlaytnTokenTransfer, self).__init__()

        self._block_timestamp: datetime = None
        self._transaction_receipt_status: int = None

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

    ### Prop: receipt_status ###
    @property
    def transaction_receipt_status(self) -> int:
        return self._transaction_receipt_status

    @transaction_receipt_status.setter
    def transaction_receipt_status(self, value) -> None:
        value = type_conversion("transaction_receipt_status", value, int)
        self._transaction_receipt_status = value

    @transaction_receipt_status.deleter
    def transaction_receipt_status(self) -> None:
        del self._transaction_receipt_status

    @staticmethod
    def enrich(
        raw_token_transfers: KlaytnRawTokenTransfer,
        block_timestamp,
        transaction_receipt_status,
    ):
        token_transfer = KlaytnTokenTransfer()

        for k, v in raw_token_transfers.__dict__.items():
            if hasattr(token_transfer, k):
                token_transfer.__setattr__(k, v)

        # transactions
        token_transfer.block_timestamp = block_timestamp

        # receipt info
        token_transfer.transaction_receipt_status = transaction_receipt_status

        return token_transfer
