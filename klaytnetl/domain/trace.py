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
)
from datetime import datetime
from decimal import Decimal
from typing import Union, Optional


class KlaytnRawTrace(BaseDomain):
    def __init__(self):
        self._block_number: int = None
        self._transaction_hash: str = None
        self._transaction_index: int = None
        self._from_address: Optional[str] = None
        self._to_address: Optional[str] = None
        self._value: Decimal = None
        self._input: str = None
        self._output: str = None
        self._trace_type: str = None
        self._call_type: str = None
        self._gas: int = None
        self._gas_used: int = None
        self._subtraces: int = 0
        self._trace_address: Optional[list] = None
        self._error: Optional[str] = None
        self._status: int = None
        self._trace_index: int = None

    ### Prop: block_number ###
    @property
    def block_number(self) -> int:
        return self._block_number

    @block_number.setter
    def block_number(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.block_number must be {int}.")

        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

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
        if not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.transaction_index must be {int}.")

        self._transaction_index = value

    @transaction_index.deleter
    def transaction_index(self) -> None:
        del self._transaction_index

    ### Prop: from_address ###
    @property
    def from_address(self) -> Optional[str]:
        return self._from_address

    @from_address.setter
    def from_address(self, value: Optional[str]) -> None:
        try:
            self._from_address = validate_address(value) if value is not None else None
        except TypeError as te:
            raise TypeError(
                f"TypeUnmatched: type error. [bn: {self._block_number}]\n" + str(te)
            )
        except ValueError as ve:
            raise ValueError(
                f"ValueNotAllowed: value error. [bn: {self._block_number}]\n" + str(ve)
            )

    @from_address.deleter
    def from_address(self) -> None:
        del self._from_address

    ### Prop: to_address ###
    @property
    def to_address(self) -> Optional[str]:
        return self._to_address

    @to_address.setter
    def to_address(self, value: Optional[str]) -> None:
        try:
            self._to_address = validate_address(value) if value is not None else None
        except TypeError as te:
            raise TypeError(
                f"TypeUnmatched: type error. [bn: {self._block_number}]\n" + str(te)
            )
        except ValueError as ve:
            raise ValueError(
                f"ValueNotAllowed: value error. [bn: {self._block_number}]\n" + str(ve)
            )

    @to_address.deleter
    def to_address(self) -> None:
        del self._to_address

    ### Prop: value ###
    @property
    def value(self) -> Decimal:
        return self._value

    @value.setter
    def value(self, value: Union[int, Decimal, None]) -> None:
        value = int_to_decimal(value)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: trace.value must be a non-negative decimal."
            )

        self._value = value

    @value.deleter
    def value(self) -> None:
        del self._value

    ### Prop: input ###
    @property
    def input(self) -> str:
        return self._input

    @input.setter
    def input(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: trace.input must be {str}.")

        self._input = value

    @input.deleter
    def input(self) -> None:
        del self._input

    ### Prop: output ###
    @property
    def output(self) -> str:
        return self._output

    @output.setter
    def output(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: trace.output must be {str}.")

        self._output = value

    @output.deleter
    def output(self) -> None:
        del self._output

    ### Prop: trace_type ###
    @property
    def trace_type(self) -> str:
        return self._trace_type

    @trace_type.setter
    def trace_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: trace.trace_type must be {str}.")

        self._trace_type = value

    @trace_type.deleter
    def trace_type(self) -> None:
        del self._trace_type

    ### Prop: call_type ###
    @property
    def call_type(self) -> str:
        return self._call_type

    @call_type.setter
    def call_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: trace.call_type must be {str}.")

        self._call_type = value

    @call_type.deleter
    def call_type(self) -> None:
        del self._call_type

    ### Prop: gas ###
    @property
    def gas(self) -> int:
        return self._gas

    @gas.setter
    def gas(self, value: int) -> None:
        if value is None:
            self._gas = 0
        elif not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.gas must be {int}.")
        else:
            self._gas = value

    @gas.deleter
    def gas(self) -> None:
        del self._gas

    ### Prop: gas_used ###
    @property
    def gas_used(self) -> int:
        return self._gas_used

    @gas_used.setter
    def gas_used(self, value: Union[int, None]) -> None:
        if value is None:
            self._gas_used = 0
        elif not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.gas_used must be {int}.")
        else:
            self._gas_used = value

    @gas_used.deleter
    def gas_used(self) -> None:
        del self._gas_used

    ### Prop: subtraces ###
    @property
    def subtraces(self) -> int:
        return self._subtraces

    @subtraces.setter
    def subtraces(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.subtraces must be {int}.")

        self._subtraces = value

    @subtraces.deleter
    def subtraces(self) -> None:
        del self._subtraces

    ### Prop: trace_address ###
    @property
    def trace_address(self) -> Optional[list]:
        return self._trace_address

    @trace_address.setter
    def trace_address(self, value: Optional[list]) -> None:
        if value is not None and not isinstance(value, list):
            raise TypeError(
                f"TypeUnmatched: trace.trace_address must be {Optional[list]}."
            )

        self._trace_address = value

    @trace_address.deleter
    def trace_address(self) -> None:
        del self._trace_address

    ### Prop: error ###
    @property
    def error(self) -> Optional[str]:
        return self._error

    @error.setter
    def error(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: trace.error must be {str}.")

        self._error = value

    @error.deleter
    def error(self) -> None:
        del self._error

    ### Prop: status ###
    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.status must be {int}.")
        if value not in {0, 1}:
            raise ValueError("ValueNotAllowed: trace.status must be 0 or 1.")

        self._status = value

    @status.deleter
    def status(self) -> None:
        del self._status

    ### Prop: trace_index ###
    @property
    def trace_index(self) -> int:
        return self._trace_index

    @trace_index.setter
    def trace_index(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError(f"TypeUnmatched: trace.trace_index must be {int}.")

        self._trace_index = value

    @trace_index.deleter
    def trace_index(self) -> None:
        del self._trace_index


class KlaytnTrace(KlaytnRawTrace):
    def __init__(self):
        super(KlaytnTrace, self).__init__()
        self._block_hash: str = None
        self._block_timestamp: datetime = None
        self._transaction_receipt_status: int = None

    ### Prop: block_hash ###
    @property
    def block_hash(self) -> str:
        return self._block_hash

    @block_hash.setter
    def block_hash(self, value) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: trace.block_hash cannot be {None}.")

        self._block_hash = value

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
        self._block_timestamp

    ### Prop: transaction_receipt_status ###
    @property
    def transaction_receipt_status(self) -> int:
        return self._transaction_receipt_status

    @transaction_receipt_status.setter
    def transaction_receipt_status(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"TypeUnmatched: trace.transaction_receipt_status must be {int}."
            )

        self._transaction_receipt_status = value

    @transaction_receipt_status.deleter
    def transaction_receipt_status(self) -> None:
        del self._transaction_receipt_status

    @staticmethod
    def enrich(
        raw_trace: KlaytnRawTrace,
        block_hash,
        block_timestamp,
        transaction_receipt_status,
    ):
        trace = KlaytnTrace()

        for k, v in raw_trace.__dict__.items():
            if hasattr(trace, k):
                trace.__setattr__(k, v)

        # timestamps
        trace.block_hash = block_hash
        trace.block_timestamp = block_timestamp

        # receipt info
        trace.transaction_receipt_status = transaction_receipt_status

        return trace
