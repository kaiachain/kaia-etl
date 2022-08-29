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
from klaytnetl.utils import float_to_datetime, validate_address
from datetime import datetime
from typing import Union


class KlaytnRawTraceBlock(BaseDomain):
    def __init__(self):
        self._block_number: int = None
        self._transaction_traces: list = []

    ### Prop: block_number ###
    @property
    def block_number(self) -> int:
        return self._block_number

    @block_number.setter
    def block_number(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError(f"TypeUnmached: trace_block.block_number must be {int}.")

        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

    ### Prop: transaction_traces ###
    @property
    def transaction_traces(self) -> list:
        return self._transaction_traces

    @transaction_traces.setter
    def transaction_traces(self, value) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmached: log.transaction_traces must be {list}.")

        self._transaction_traces = value

    @transaction_traces.deleter
    def transaction_traces(self) -> None:
        del self._transaction_traces


class KlaytnTraceBlock(KlaytnRawTraceBlock):
    def __init__(self):
        super(KlaytnTraceBlock, self).__init__()
        self._block_hash: str = None
        self._block_timestamp: datetime = None

    ### Prop: block_hash ###
    @property
    def block_hash(self) -> str:
        return self._block_hash

    @block_hash.setter
    def block_hash(self, value) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmached: trace_block.block_hash cannot be {None}.")

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

    @staticmethod
    def enrich(raw_trace_block: KlaytnRawTraceBlock, block_hash, block_timestamp):
        trace_block = KlaytnTraceBlock()

        # duplicated field values
        for k, v in raw_trace_block.__dict__.items():
            if hasattr(trace_block, k):
                trace_block.__setattr__(k, v)

        # append additional fields
        trace_block.block_hash = block_hash
        trace_block.block_timestamp = block_timestamp

        return trace_block
