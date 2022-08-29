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


import pytest

from klaytnetl.utils import int_to_decimal, float_to_datetime, validate_address
from datetime import datetime, timezone
from decimal import Decimal


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (3, Decimal(3)),
        (Decimal(3), Decimal(3)),
        (None, 0),
    ],
)
def test_int_to_decimal(test_input, expected):
    assert int_to_decimal(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            1574770789.019,
            datetime(2019, 11, 26, 12, 19, 49, 19000, tzinfo=timezone.utc),
        ),
        (1574770789, datetime(2019, 11, 26, 12, 19, 49, tzinfo=timezone.utc)),
        (
            datetime(2019, 11, 26, 12, 19, 49, 19000, tzinfo=timezone.utc),
            datetime(2019, 11, 26, 12, 19, 49, 19000, tzinfo=timezone.utc),
        ),
    ],
)
def test_float_to_datetime(test_input, expected):
    assert float_to_datetime(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected,digits",
    [
        (
            "0xc032c34cb9fe064fe435199e1078dd8756a166b5",
            "0xc032c34cb9fe064fe435199e1078dd8756a166b5",
            42,
        ),
        (
            "0x8955fe422a68babf0a83941ae18e97720ad4c2960c15e12745924af56042434c",
            "0x8955fe422a68babf0a83941ae18e97720ad4c2960c15e12745924af56042434c",
            66,
        ),
    ],
)
def test_validate_address(test_input, expected, digits):
    assert validate_address(test_input, digits) == expected
