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
from typing import Union


class KlaytnRawBlock(BaseDomain):
    def __init__(self):
        self._number: int = None
        self._hash: str = None
        self._parent_hash: str = None
        self._logs_bloom: str = None
        self._transactions_root: str = None
        self._state_root: str = None
        self._receipts_root: str = None

        self._size: int = None
        self._extra_data: str = None
        self._gas_used: Union[int, Decimal, None] = None
        self._timestamp: datetime = None

        self._transactions: list = []
        self._transaction_count: int = 0

        self._receipts: list = []

        self._block_score: int = None
        self._total_block_score: int = None

        self._governance_data: str = None  # Data: RLP encoded data
        self._vote_data: str = None  # Data: RLP encoded data

        self._committee: list = []
        self._proposer: str = None
        self._reward_address: str = None

        self._base_fee_per_gas: Union[int, Decimal, None] = None

    ### Prop: number ###
    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        value = type_conversion("block.number", value, int)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: block.number must be a non-negative integer."
            )

        self._number = value

    @number.deleter
    def number(self) -> None:
        del self._number

    ### Prop: hash ###
    @property
    def hash(self) -> str:
        return self._hash

    @hash.setter
    def hash(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.hash cannot be {None}.")

        self._hash = value

    @hash.deleter
    def hash(self) -> None:
        del self._hash

    ### Prop: parent_hash ###
    @property
    def parent_hash(self) -> str:
        return self._parent_hash

    @parent_hash.setter
    def parent_hash(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.parent_hash cannot be {None}.")

        self._parent_hash = value

    @parent_hash.deleter
    def parent_hash(self) -> None:
        del self._parent_hash

    ### Prop: logs_bloom ###
    @property
    def logs_bloom(self) -> str:
        return self._logs_bloom

    @logs_bloom.setter
    def logs_bloom(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: block.log_bloom must be {str}.")

        self._logs_bloom = value

    @logs_bloom.deleter
    def logs_bloom(self) -> None:
        del self._logs_bloom

    ### Prop: transactions_root ###
    @property
    def transactions_root(self) -> str:
        return self._transactions_root

    @transactions_root.setter
    def transactions_root(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.transactions_root cannot be {None}.")

        self._transactions_root = value

    @transactions_root.deleter
    def transactions_root(self) -> None:
        del self._transactions_root

    ### Prop: state_root ###
    @property
    def state_root(self) -> str:
        return self._state_root

    @state_root.setter
    def state_root(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.state_root cannot be {None}.")

        self._state_root = value

    @state_root.deleter
    def state_root(self) -> None:
        del self._state_root

    ### Prop: receipts_root ###
    @property
    def receipts_root(self) -> str:
        return self._receipts_root

    @receipts_root.setter
    def receipts_root(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.receipts_root cannot be {None}.")

        self._receipts_root = value

    @receipts_root.deleter
    def receipts_root(self) -> None:
        del self._receipts_root

    ### Prop: size ###
    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        value = type_conversion("block.size", value, int)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: block.size must be a non-negative integer."
            )

        self._size = value

    @size.deleter
    def size(self) -> None:
        del self._size

    ### Prop: extra_data ###
    @property
    def extra_data(self) -> str:
        return self._extra_data

    @extra_data.setter
    def extra_data(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: block.extra_data must be {str}.")

        self._extra_data = value

    @extra_data.deleter
    def extra_data(self) -> None:
        del self._extra_data

    ### Prop: gas_used ###
    @property
    def gas_used(self) -> Union[int, Decimal, None]:
        return self._gas_used

    @gas_used.setter
    def gas_used(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            value = 0
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: block.gas_used must be a non-negative decimal."
                )

        self._gas_used = value

    @gas_used.deleter
    def gas_used(self) -> None:
        del self._gas_used

    ### Prop: timestamp ###
    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Union[datetime, float, int]) -> None:
        self._timestamp = float_to_datetime(value)

    @timestamp.deleter
    def timestamp(self) -> None:
        del self._timestamp

    ### Prop: transactions ###
    @property
    def transactions(self) -> list:
        return self._transactions

    @transactions.setter
    def transactions(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: block.transactions must be {list}.")

        self._transactions = value

    @transactions.deleter
    def transactions(self) -> None:
        del self._transactions

    ### Prop: transaction_count ###
    @property
    def transaction_count(self) -> int:
        return self._transaction_count

    @transaction_count.setter
    def transaction_count(self, value: int) -> None:
        value = type_conversion("block.transaction_count", value, int)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: block.transaction_count must be a non-negative integer."
            )

        self._transaction_count = value

    @transaction_count.deleter
    def transaction_count(self) -> None:
        del self._transaction_count

    ### Prop: receipts ###
    @property
    def receipts(self) -> list:
        return self._receipts

    @receipts.setter
    def receipts(self, value: str) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: block.receipts must be {list}.")

        self._receipts = value

    @receipts.deleter
    def receipts(self) -> None:
        del self._receipts

    ### Prop: block_score ###
    @property
    def block_score(self) -> int:
        return self._block_score

    @block_score.setter
    def block_score(self, value: int) -> None:
        value = type_conversion("block.block_score", value, int)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: block.block_score must be a non-negative integer."
            )

        self._block_score = value

    @block_score.deleter
    def block_score(self) -> None:
        del self._block_score

    ### Prop: total_block_score ###
    @property
    def total_block_score(self) -> int:
        return self._total_block_score

    @total_block_score.setter
    def total_block_score(self, value: int) -> None:
        value = type_conversion("block.total_block_score", value, int)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: block.total_block_score must be a non-negative integer."
            )

        self._total_block_score = value

    @total_block_score.deleter
    def total_block_score(self) -> None:
        del self._total_block_score

    ### Prop: governance_data ###
    @property
    def governance_data(self) -> str:
        return self._governance_data

    @governance_data.setter
    def governance_data(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: block.governance_data must be {str}.")

        self._governance_data = value

    @governance_data.deleter
    def governance_data(self) -> None:
        del self._governance_data

    ### Prop: vote_data ###
    @property
    def vote_data(self) -> str:
        return self._vote_data

    @vote_data.setter
    def vote_data(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: block.vote_data must be {str}.")

        self._vote_data = value

    @vote_data.deleter
    def vote_data(self) -> None:
        del self._vote_data

    ### Prop: committee ###
    @property
    def committee(self) -> list:
        return self._committee

    @committee.setter
    def committee(self, value: list) -> None:
        if value is None:  # when block is zero
            self._committee = value
        elif not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: block.committee must be {list}.")

        self._committee = value

    @committee.deleter
    def committee(self) -> None:
        del self._committee

    ### Prop: proposer ###
    @property
    def proposer(self) -> str:
        return self._proposer

    @proposer.setter
    def proposer(self, value: str) -> None:
        value = validate_address(value, digits=42)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.proposer cannot be {None}.")

        self._proposer = value

    @proposer.deleter
    def proposer(self) -> None:
        del self._proposer

    ### Prop: reward_address ###
    @property
    def reward_address(self) -> str:
        return self._reward_address

    @reward_address.setter
    def reward_address(self, value: str) -> None:
        value = validate_address(value, digits=42)
        if value is None:
            raise TypeError(f"TypeUnmatched: block.reward_address cannot be {None}.")

        self._reward_address = value

    @reward_address.deleter
    def reward_address(self) -> None:
        del self._reward_address

    ### Prop: base_fee_per_gas ###
    @property
    def base_fee_per_gas(self) -> Union[int, Decimal, None]:
        return self._base_fee_per_gas

    @base_fee_per_gas.setter
    def base_fee_per_gas(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            self._base_fee_per_gas = None
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: block.base_fee_per_gas must be a non-negative decimal."
                )
            self._base_fee_per_gas = value

    @base_fee_per_gas.deleter
    def base_fee_per_gas(self) -> None:
        del self._base_fee_per_gas


class KlaytnBlock(KlaytnRawBlock):
    def __init__(self):
        super(KlaytnBlock, self).__init__()

    @staticmethod
    def enrich(raw_block: KlaytnRawBlock):
        block = KlaytnBlock()

        for k, v in raw_block.__dict__.items():
            if hasattr(block, k):
                block.__setattr__(k, v)

        return block
