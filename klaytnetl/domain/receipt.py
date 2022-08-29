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


from decimal import Decimal

from klaytnetl.domain.base import BaseDomain
from klaytnetl.utils import validate_address, type_conversion, int_to_decimal
from typing import Union, Optional


class KlaytnRawReceipt(BaseDomain):
    def __init__(self):
        self._transaction_hash: str = None
        self._transaction_index: int = None
        self._block_hash: str = None
        self._block_number: int = None
        self._contract_address: Optional[str] = None
        self._logs: list = []
        self._status: int = None
        self._effective_gas_price: Union[int, Decimal, None] = None
        self._gas: Union[int, Decimal, None] = None
        self._gas_price: Union[int, Decimal, None] = None
        self._gas_used: Union[int, Decimal, None] = None
        self._logs_bloom: str = None
        self._nonce: int = None
        self._fee_payer: Optional[str] = None
        self._fee_payer_signatures: Optional[list] = []
        self._fee_ratio: Optional[int] = None
        self._code_format: Optional[str] = None
        self._human_readable: Optional[bool] = None
        self._tx_error: Optional[str] = None
        self._key: Optional[str] = None
        self._input_data: Optional[str] = None
        self._from_address: str = None
        self._to_address: Optional[str] = None
        self._type_name: str = None
        self._type_int: int = None
        self._sender_tx_hash: str = None
        self._signatures: list = []
        self._value: Union[None, int, Decimal] = None
        self._input_json: Optional[dict] = None
        self._access_list: Optional[list] = []
        self._chain_id: Optional[int] = None
        self._max_priority_fee_per_gas: Union[int, Decimal, None] = None
        self._max_fee_per_gas: Union[int, Decimal, None] = None

    ### Prop: transaction_hash ###
    @property
    def transaction_hash(self) -> str:
        return self._transaction_hash

    @transaction_hash.setter
    def transaction_hash(self, value: str) -> None:
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(
                f"TypeUnmatched: receipt.transaction_hash cannot be {None}."
            )

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
        value = type_conversion("receipt.transaction_index", value, int)
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
        value = validate_address(value, digits=66)
        if value is None:
            raise TypeError(f"TypeUnmatched: receipt.block_hash cannot be {None}.")

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
        value = type_conversion("receipt.block_number", value, int)
        self._block_number = value

    @block_number.deleter
    def block_number(self) -> None:
        del self._block_number

    ### Prop: contract_address ###
    @property
    def contract_address(self) -> Optional[str]:
        return self._contract_address

    @contract_address.setter
    def contract_address(self, value: Optional[str]) -> None:
        self._contract_address = (
            validate_address(value, digits=42) if value is not None else None
        )

    @contract_address.deleter
    def contract_address(self) -> None:
        del self._contract_address

    ### Prop: logs ###
    @property
    def logs(self) -> list:
        return self._logs

    @logs.setter
    def logs(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(f"TypeUnmatched: receipt.logs must be {list}.")

        self._logs = value

    @logs.deleter
    def logs(self) -> None:
        del self._logs

    ### Prop: status ###
    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int) -> None:
        value = type_conversion("receipt.status", value, int)
        self._status = value

    @status.deleter
    def status(self) -> None:
        del self._status

    ### Prop: effective gas price ###
    @property
    def effective_gas_price(self) -> Union[int, Decimal, None]:
        return self._effective_gas_price

    @effective_gas_price.setter
    def effective_gas_price(self, value: Union[int, Decimal, None]) -> None:
        if value is None:
            self._effective_gas_price = self._gas_price
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: receipt.effective_gas_price must be a non-negative decimal."
                )
            self._effective_gas_price = value

    @effective_gas_price.deleter
    def effective_gas_price(self) -> None:
        del self._effective_gas_price

    ### Prop: gas ###
    @property
    def gas(self) -> Union[int, Decimal, None]:
        return self._gas

    @gas.setter
    def gas(self, value: Union[int, Decimal, None]) -> None:
        value = int_to_decimal(value)
        if value < 0:
            raise ValueError(
                "ValueNotAllowed: receipt.gas must be a non-negative decimal."
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
                "ValueNotAllowed: receipt.gas_price must be a non-negative decimal."
            )

        self._gas_price = value

    @gas_price.deleter
    def gas_price(self) -> None:
        del self._gas_price

    ### Prop: gas used ###
    @property
    def gas_used(self) -> Union[None, int, Decimal]:
        return self._gas_used

    @gas_used.setter
    def gas_used(self, value: Union[None, int, Decimal]) -> None:
        if value is None:
            value = 0
        else:
            value = int_to_decimal(value)
            if value < 0:
                raise ValueError(
                    "ValueNotAllowed: receipt.gas_used must be a non-negative decimal."
                )

        self._gas_used = value

    @gas_used.deleter
    def gas_used(self) -> None:
        del self._gas_used

    ### Prop: logs bloom ###
    @property
    def logs_bloom(self) -> str:
        return self._logs_bloom

    @logs_bloom.setter
    def logs_bloom(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: receipt.logs_bloom must be {str}.")

        self._logs_bloom = value

    @logs_bloom.deleter
    def logs_bloom(self) -> None:
        del self._logs_bloom

    ### Prop: nonce ###
    @property
    def nonce(self) -> int:
        return self._nonce

    @nonce.setter
    def nonce(self, value: int) -> None:
        value = type_conversion("receipt.nonce", value, int)
        self._nonce = value

    @nonce.deleter
    def nonce(self) -> None:
        del self._nonce

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
    def fee_payer_signatures(self) -> Optional[list]:
        return (
            self._fee_payer_signatures if self._fee_payer_signatures is not None else []
        )

    @fee_payer_signatures.setter
    def fee_payer_signatures(self, value: Optional[list]) -> None:
        if value is not None and not isinstance(value, list):
            raise TypeError(
                f"TypeUnmatched: receipt.fee_payer_signatures must be {Optional[list]}."
            )

        self._fee_payer_signatures = value

    @fee_payer_signatures.deleter
    def fee_payer_signatures(self) -> None:
        del self._fee_payer_signatures

    ### Prop: fee ratio ###
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
            value = type_conversion("receipt.fee_ratio", value, int)
            if value < 0 or value > 100:
                raise ValueError(
                    "ValueNotAllowed: receipt.fee_ratio must be an integer between 0 and 100, "
                    "inclusively."
                )
            else:
                self._fee_ratio = value

    @fee_ratio.deleter
    def fee_ratio(self) -> None:
        del self._fee_ratio

    ### Prop: code format ###
    @property
    def code_format(self) -> Optional[str]:
        return self._code_format

    @code_format.setter
    def code_format(self, value: Optional[str]) -> None:
        if not isinstance(value, str) and value:
            raise TypeError(f"TypeUnmatched: receipt.code_format must be {str}.")

        self._code_format = value

    @code_format.deleter
    def code_format(self) -> None:
        del self._code_format

    ### Prop: human readable ###
    @property
    def human_readable(self) -> Optional[bool]:
        return self._human_readable

    @human_readable.setter
    def human_readable(self, value: Optional[bool]) -> None:
        if not isinstance(value, bool) and value:
            raise TypeError(f"TypeUnmatched: receipt.human_readable must be {bool}.")

        self._human_readable = value

    @human_readable.deleter
    def human_readable(self) -> None:
        del self._human_readable

    ### Prop: tx error ###
    @property
    def tx_error(self) -> Optional[str]:
        return self._tx_error

    @tx_error.setter
    def tx_error(self, value: Optional[str]) -> None:
        if not isinstance(value, str) and value:
            raise TypeError(f"TypeUnmatched: receipt.tx_error must be {str}.")

        self._tx_error = value

    @tx_error.deleter
    def tx_error(self) -> None:
        del self._tx_error

    ### Prop: key ###
    @property
    def key(self) -> Optional[str]:
        return self._key

    @key.setter
    def key(self, value: Optional[str]) -> None:
        if not isinstance(value, str) and value:
            raise TypeError(f"TypeUnmatched: receipt.key must be {str}.")

        self._key = value

    @key.deleter
    def key(self) -> None:
        del self._key

    ### Prop: input data ###
    @property
    def input_data(self) -> Optional[str]:
        return self._input_data

    @input_data.setter
    def input_data(self, value: Optional[str]) -> None:
        if not isinstance(value, str) and value:
            raise TypeError(f"TypeUnmatched: receipt.input_data must be {str}.")

        self._input_data = value

    @input_data.deleter
    def input_data(self) -> None:
        del self._input_data

    ### Prop: from address ###
    @property
    def from_address(self) -> str:
        return self._from_address

    @from_address.setter
    def from_address(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: receipt.from_address must be {str}.")

        self._from_address = value

    @from_address.deleter
    def from_address(self) -> None:
        del self._from_address

    ### Prop: to address ###
    @property
    def to_address(self) -> str:
        return self._to_address

    @to_address.setter
    def to_address(self, value: str) -> None:
        if not isinstance(value, str) and value:
            raise TypeError(f"TypeUnmatched: receipt.to_address must be {str}.")

        self._to_address = value

    @to_address.deleter
    def to_address(self) -> None:
        del self._to_address

    ### Prop: type name ###
    @property
    def type_name(self) -> str:
        return self._type_name

    @type_name.setter
    def type_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: receipt.type_name must be {str}.")

        self._type_name = value

    @type_name.deleter
    def type_name(self) -> None:
        del self._type_name

    ### Prop: type int ###
    @property
    def type_int(self) -> int:
        return self._type_int

    @type_int.setter
    def type_int(self, value: int) -> None:
        type_conversion("receipt.type_int", value, int)
        self._type_int = value

    @type_int.deleter
    def type_int(self) -> None:
        del self._type_int

    ### Prop: sender_tx_hash ###
    @property
    def sender_tx_hash(self) -> str:
        return self._sender_tx_hash

    @sender_tx_hash.setter
    def sender_tx_hash(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"TypeUnmatched: receipt.sender_tx_hash must be {str}.")

        self._sender_tx_hash = value

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
            raise TypeError(f"TypeUnmatched: receipt.signatures must be {list}.")

        self._signatures = value

    @signatures.deleter
    def signatures(self) -> None:
        del self._signatures

    ### Prop: value quantity ###
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
                    "ValueNotAllowed: token_transfer.value must be a non-negative decimal."
                )
            self._value = value

    @value.deleter
    def value(self) -> None:
        del self._value

    ### Prop: input json ###
    @property
    def input_json(self) -> Optional[dict]:
        return self._input_json

    @input_json.setter
    def input_json(self, value: Optional[dict]) -> None:
        if not isinstance(value, dict) and value:
            raise TypeError(f"TypeUnmatched: receipt.input_json must be {dict}.")

        self._input_json = value

    @input_json.deleter
    def input_json(self) -> None:
        del self._input_json

    ### Prop: access list ###
    @property
    def access_list(self) -> Optional[list]:
        return self._access_list if self._access_list is not None else []

    @access_list.setter
    def access_list(self, value: Optional[list]) -> None:
        if not isinstance(value, list) and value:
            raise TypeError(f"TypeUnmatched: receipt.access_list must be {list}.")

        self._access_list = value

    @access_list.deleter
    def access_list(self) -> None:
        del self._access_list

    ### Prop: chain id ###
    @property
    def chain_id(self) -> Optional[int]:
        return self._chain_id

    @chain_id.setter
    def chain_id(self, value: Optional[int]) -> None:
        type_conversion("receipt.chain_id", value, int)
        self._chain_id = value

    @chain_id.deleter
    def chain_id(self) -> None:
        del self._chain_id

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
                    "ValueNotAllowed: receipt.max_priority_fee_per_gas"
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
                    "ValueNotAllowed: receipt.max_fee_per_gas must be a non-negative decimal."
                )
            self._max_fee_per_gas = value

    @max_fee_per_gas.deleter
    def max_fee_per_gas(self) -> None:
        del self._max_fee_per_gas
