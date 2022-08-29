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
from klaytnetl.utils import float_to_datetime, validate_address, type_conversion
from datetime import datetime
from typing import Union


class KlaytnRawReceiptLog(BaseDomain):
    def __init__(self):
        self._log_index: int = None
        self._transaction_hash: str = None
        self._transaction_index: int = None
        self._block_hash: str = None
        self._block_number: int = None
        self._address: str = None
        self._data: str = None
        self._topics: list = []
        self._removed: bool = []

    ### Prop: log_index ###
    @property
    def log_index(self) -> int:
        return self._log_index

    @log_index.setter
    def log_index(self, value: int) -> None:
        value = type_conversion("log.log_index", value, int)
        self._log_index = int(value)

    @log_index.deleter
    def log_index(self) -> None:
        del self._log_index

    ### Prop: transaction_hash ###
    @property
    def transaction_hash(self) -> str:
        return self._transaction_hash

    @transaction_hash.setter
    def transaction_hash(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: log.transaction_hash cannot be {None}.")

        self._transaction_hash = value

    @transaction_hash.deleter
    def transaction_hash(self) -> None:
        del self._transaction_hash

    ### Prop: transaction_index ###
    @property
    def transaction_index(self) -> int:
        return self._transaction_index

    @transaction_index.setter
    def transaction_index(self, value: int) -> None:
        value = type_conversion("log.transaction_index", value, int)
        self._transaction_index = int(value)

    @transaction_index.deleter
    def transaction_index(self) -> None:
        del self._transaction_index

    ### Prop: block_hash ###
    @property
    def block_hash(self) -> str:
        return self._block_hash

    @block_hash.setter
    def block_hash(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: log.block_hash cannot be {None}.")

        self._block_hash = value

    @block_hash.deleter
    def block_hash(self) -> None:
        del self._block_hash

    ### Prop: block_number ###
    @property
    def block_number(self) -> int:
        return self._block_number

    @block_number.setter
    def block_number(self, value: int) -> None:
        value = type_conversion("log.block_number", value, int)
        self._block_number = int(value)

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

    ### Prop: address ###
    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        value = validate_address(value, digits=42)
        if value is None:
            raise TypeError(f"TypeUnmatched: log.address cannot be {None}.")

        self._address = value

    @address.deleter
    def address(self) -> None:
        del self._address

    ### Prop: data ###
    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: log.data must be {str}.")

        self._data = value

    @data.deleter
    def data(self) -> None:
        del self._data

    ### Prop: topics ###
    @property
    def topics(self) -> list:
        return self._topics

    @topics.setter
    def topics(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: log.topics must be {list}.")

        self._topics = value

    @topics.deleter
    def topics(self) -> None:
        del self._topics

    ### Prop: removed ###
    @property
    def removed(self) -> list:
        return self._removed

    @removed.setter
    def removed(self, value: bool) -> None:
        value = type_conversion("log.removed", value, bool)
        self._removed = bool(value)

    @removed.deleter
    def removed(self) -> None:
        del self._removed


class KlaytnReceiptLog(KlaytnRawReceiptLog):
    def __init__(self):
        super(KlaytnReceiptLog, self).__init__()

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
    def transaction_receipt_status(self, value: int) -> None:
        value = type_conversion("log.transaction_receipt", value, int)
        self._transaction_receipt_status = value

    @transaction_receipt_status.deleter
    def transaction_receipt_status(self) -> None:
        del self._transaction_receipt_status

    @staticmethod
    def enrich(
        raw_logs: KlaytnRawReceiptLog, block_timestamp, transaction_receipt_status
    ):
        log = KlaytnReceiptLog()

        for k, v in raw_logs.__dict__.items():
            if hasattr(log, k):
                log.__setattr__(k, v)

        # transactions
        log.block_timestamp = block_timestamp

        # receipt info
        log.transaction_receipt_status = transaction_receipt_status

        return log
