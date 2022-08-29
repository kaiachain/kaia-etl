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


from datetime import datetime, timezone
import dateutil.parser

import pytz

import itertools
from typing import Union
from decimal import Decimal

from klaytnetl.misc.retriable_value_error import RetriableValueError


def hex_to_dec(hex_string):
    if hex_string is None:
        return None
    try:
        return int(hex_string, 16)
    except ValueError:
        print("Not a hex string %s" % hex_string)
        return hex_string


def to_int_or_none(val):
    if isinstance(val, int):
        return val
    if val is None or val == "":
        return None
    try:
        return int(val)
    except ValueError:
        return None


def chunk_string(string, length):
    return (string[0 + i: length + i] for i in range(0, len(string), length))


def to_normalized_address(address):
    if address is None or not isinstance(address, str):
        return address
    return address.lower()


def validate_range(range_start_incl, range_end_incl):
    if range_start_incl < 0 or range_end_incl < 0:
        raise ValueError("range_start and range_end must be greater or equal to 0")

    if range_end_incl < range_start_incl:
        raise ValueError("range_end must be greater or equal to range_start")


def rpc_response_batch_to_results(response):
    for response_item in response:
        yield rpc_response_to_result(response_item)


def rpc_response_to_result(response):
    result = response.get("result")
    if result is None:
        error_message = "result is None in response {}.".format(response)
        # klaytn cypress block 1 & 2 has message results parent 0000000000000000000000000000000000000000000000000000000000000000 not found.
        # if we don't skip this 2 blocks for traces, it will not run the next blocks and keep on retrying the same error message.
        if (
            response.get("error").get("message")
            == "parent 0000000000000000000000000000000000000000000000000000000000000000 not found"
        ):
            return []
        if response.get("error") is None:
            error_message = error_message + " Make sure Klaytn node is synced."
            # When nodes are behind a load balancer it makes sense to retry the request in hopes it will go to other,
            # synced node
            raise RetriableValueError(error_message)
        elif response.get("error") is not None and is_retriable_error(
            response.get("error").get("code")
        ):
            raise RetriableValueError(error_message)
        raise ValueError(error_message)
    return result


def is_retriable_error(error_code):
    if error_code is None:
        return False

    if not isinstance(error_code, int):
        return False

    # https://www.jsonrpc.org/specification#error_object
    if error_code == -32603 or (-32000 >= error_code >= -32099):
        return True

    return False


def split_to_batches(start_incl, end_incl, batch_size):
    """start_incl and end_incl are inclusive, the returned batch ranges are also inclusive"""
    for batch_start in range(start_incl, end_incl + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_incl)
        yield batch_start, batch_end


def dynamic_batch_iterator(iterable, batch_size_getter):
    batch = []
    batch_size = batch_size_getter()
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
            batch_size = batch_size_getter()
    if len(batch) > 0:
        yield batch


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def strf_unix_dt(
    unix_timestamp: Union[int, float], format: str = None, tzinfo=None
) -> str:
    """unix timestamp to string formatted timestamp with tz

    Returns
    -------
    strf_timestamp: str
        ISO standard format string for datetime with timezone (default: UTC)
    """

    if not isinstance(unix_timestamp, (int, float)):
        raise ValueError("unix_timestamp must be integer or float")

    if unix_timestamp < 0:
        raise ValueError("unix_timestamp must be greater or equal to 0")

    timestamp = datetime.utcfromtimestamp(unix_timestamp)

    if tzinfo is not None:
        timestamp_with_tz = pytz.timezone(tzinfo).localize(timestamp)
    else:
        timestamp_with_tz = pytz.utc.localize(timestamp)

    return timestamp_with_tz.isoformat(sep="T")


def strp_unix_dt(strf_timestamp: str, fmt: str = None) -> Union[int, float]:
    """string formatted timestamp to unix timestamp

    Parameters
    ----------
    strf_timestamp : str
        String formatted timestamp
    fmt : str, optional
        format string to parse the strf_timestamp, by default None

    Returns
    -------
    str
        [description]
    """
    if fmt is None:
        dt = dateutil.parser.parse(strf_timestamp)
    else:
        dt = datetime.strptime(strf_timestamp, fmt)

    return float(dt.strftime("%s.%f"))


def is_full_block(json_dict: dict) -> bool:
    return "proposer" in json_dict or "committee" in json_dict


def is_transaction_with_receipt(json_dict: dict) -> bool:
    return "logs" in json_dict


def is_contract_creation_trace(trace) -> bool:
    return (
        trace.trace_type == "create"
        and trace.to_address is not None
        and len(trace.to_address) > 0
        and trace.status == 1
    )


def type_conversion(name, value, type):
    if not value:  # Null cases
        return value
    try:
        value = type(value)
        return value
    except (ValueError, TypeError):
        raise TypeError(f"TypeUnmatched: {name} must be {type}.")


def int_to_decimal(value: Union[None, int, Decimal], fillna: int = 0) -> Decimal:
    if value is None:
        return Decimal(fillna)
    elif not isinstance(value, (int, Decimal)):
        raise TypeError(
            f"TypeUnmatched: int_to_decimal only allows following types: {Union[None, int, Decimal]}."
        )
    else:
        return Decimal(value)


def float_to_datetime(
    value: Union[datetime, float, int], tzinfo=timezone.utc
) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=tzinfo)
    elif isinstance(value, (float, int)):
        return datetime.utcfromtimestamp(value).replace(tzinfo=tzinfo)
    else:
        raise TypeError(
            f"TypeUnmatched: float_to_datetime only allows following types: {Union[datetime, float, int]}."
        )


def validate_address(value: str, digits=42) -> str:
    if value is None:
        raise TypeError(f"TypeUnmatched: a value parameter cannot be {None}.")
    elif not isinstance(value, str):
        raise TypeError(
            f"TypeUnmatched: validate_address(digits={digits}) only allows following types: {str}."
        )
    elif len(value) != digits or value[0:2] != "0x":
        raise ValueError(
            f"ValueNotAllowed: validate_address(digits={digits}) only allows a {digits}-character hex string."
        )
    else:
        return value.lower()


def is_empty_trace_result(trace_result) -> bool:
    return (
        trace_result.get("type") == 0
        and trace_result.get("from") == "0x"
        and trace_result.get("to") == "0x"
        and trace_result.get("value") == "0x0"
        and trace_result.get("gas") == "0x0"
        and trace_result.get("gasUsed") == "0x0"
        and trace_result.get("input") == "0x"
        and trace_result.get("output") == "0x"
        and trace_result.get("time") == 0
    )


def return_provider(network) -> str:
    if network.lower() == "baobab":
        return "https://baobab.fandom.finance/archive"
    elif network.lower() == "cypress":
        return "https://cypress.fandom.finance/archive"
    else:
        raise ValueError(
            "Value Not Allowed: return_provider only allows either baobab or cypress"
        )
