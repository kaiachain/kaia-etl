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
from klaytnetl.web3_utils import build_web3

import tests.resources
from klaytnetl.jobs.export_tokens_job import ExportTokensJob
from klaytnetl.jobs.exporters.tokens_item_exporter import tokens_item_exporter
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)

RESOURCE_GROUP = "test_export_tokens_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "token_addresses,resource_group,web3_provider_type",
    [
        (["0x9e481eb17d3c3c07d7a6ab571b4ba8ef432b5cf2"], "erc20_tokens", "mock"),  # MCC
        (
            ["0xb88168dde0001be8546c70c117ab9e41e28f7164"],
            "erc721_tokens",
            "mock",
        ),  # PNFT
        skip_if_slow_tests_disabled(
            (["0x4e16e2567dd332d4c44474f8b8d3130b5c311cf7"],
                "erc1155_tokens",
                "fantrie",)
        ),  # ChickiFarm Ornaments
        skip_if_slow_tegsts_disabled(
            (["0x9e481eb17d3c3c07d7a6ab571b4ba8ef432b5cf2"], "erc20_tokens", "fantrie")
        ),
    ],
)
def test_export_tokens_job(tmpdir, token_addresses, resource_group, web3_provider_type):
    output_file = str(tmpdir.join("tokens.json"))

    job = ExportTokensJob(
        token_addresses_iterable=token_addresses,
        web3=ThreadLocalProxy(
            lambda: build_web3(
                get_web3_provider(
                    web3_provider_type, lambda file: read_resource(resource_group, file)
                )
            )
        ),
        item_exporter=tokens_item_exporter(output_file),
        max_workers=5,
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_tokens.json"), read_file(output_file)
    )
