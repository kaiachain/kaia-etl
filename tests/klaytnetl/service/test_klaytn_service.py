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


import os

import pytest
from dateutil.parser import parse
from web3 import HTTPProvider

from klaytnetl.service.klaytn_service import KlaytnService
from klaytnetl.service.graph_operations import OutOfBoundsError
from klaytnetl.web3_utils import build_web3
from tests.helpers import skip_if_slow_tests_disabled


@pytest.mark.parametrize(
    "date,expected_start_block,expected_end_block",
    [
        skip_if_slow_tests_disabled(["2019-06-25", 0, 44349]),
        skip_if_slow_tests_disabled(["2020-05-05", 27059553, 27145870]),
        skip_if_slow_tests_disabled(["2021-06-01", 60783182, 60869580]),
        skip_if_slow_tests_disabled(["2022-03-11", 85083893, 85169674]),
    ],
)
def test_get_block_range_for_date(date, expected_start_block, expected_end_block):
    klaytn_service = get_new_klaytn_service()
    parsed_date = parse(date)
    blocks = klaytn_service.get_block_range_for_date(parsed_date)
    assert blocks == (expected_start_block, expected_end_block)


@pytest.mark.parametrize(
    "date",
    [
        skip_if_slow_tests_disabled(["2015-07-29"]),
        skip_if_slow_tests_disabled(["2030-01-01"]),
    ],
)
def test_get_block_range_for_date_fail(date):
    klaytn_service = get_new_klaytn_service()
    parsed_date = parse(date)
    with pytest.raises(OutOfBoundsError):
        klaytn_service.get_block_range_for_date(parsed_date)


@pytest.mark.parametrize(
    "start_timestamp,end_timestamp,expected_start_block,expected_end_block",
    [
        skip_if_slow_tests_disabled([1652547600, 1652634000, 90657877, 90744232]),
        skip_if_slow_tests_disabled([1577631600, 1577718000, 16164261, 16250657]),
    ],
)
def test_get_block_range_for_timestamps(
    start_timestamp, end_timestamp, expected_start_block, expected_end_block
):
    klaytn_service = get_new_klaytn_service()
    blocks = klaytn_service.get_block_range_for_timestamps(
        start_timestamp, end_timestamp
    )
    assert blocks == (expected_start_block, expected_end_block)


def get_new_klaytn_service():
    provider_url = os.environ.get(
        "PROVIDER_URL", "https://archive-en.node.kaia.io"
    )
    web3 = build_web3(HTTPProvider(provider_url))
    return KlaytnService(web3)
