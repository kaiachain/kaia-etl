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

import tests.resources
from klaytnetl.jobs.export_block_group_job import ExportBlockGroupJob
from klaytnetl.jobs.exporters.raw_block_group_item_exporter import (
    raw_block_group_item_exporter,
)
from klaytnetl.jobs.exporters.enrich_block_group_item_exporter import (
    enrich_block_group_item_exporter,
)
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)

RESOURCE_GROUP = "test_export_block_groups_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "start_block,end_block,enrich,batch_size,resource_group,web3_provider_type",
    [
        skip_if_slow_tests_disabled(
            (88000000, 88000001, True, 1, "block_groups_enrich", "fantrie")
        ),
        skip_if_slow_tests_disabled(
            (88000000, 88000001, False, 1, "block_groups_raw", "fantrie")
        ),
    ],
)
def test_export_block_groups_job(
    tmpdir,
    start_block,
    end_block,
    enrich,
    batch_size,
    resource_group,
    web3_provider_type,
):
    blocks_output_file = str(tmpdir.join("actual_blocks.json"))
    transactions_output_file = str(tmpdir.join("actual_transactions.json"))
    receipts_output_file = str(tmpdir.join("actual_receipts.json"))
    logs_output_file = str(tmpdir.join("actual_logs.json"))
    token_transfers_output_file = str(tmpdir.join("actual_token_transfers.json"))

    if enrich:
        exporter = enrich_block_group_item_exporter(
            blocks_output_file,
            transactions_output_file,
            receipts_output_file,
            logs_output_file,
            token_transfers_output_file,
        )
    else:
        exporter = raw_block_group_item_exporter(
            blocks_output_file,
            transactions_output_file,
            receipts_output_file,
            logs_output_file,
            token_transfers_output_file,
        )

    job = ExportBlockGroupJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        enrich=enrich,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(
                web3_provider_type,
                lambda file: read_resource(resource_group, file),
                batch=True,
            )
        ),
        max_workers=5,
        item_exporter=exporter,
        export_blocks=blocks_output_file is not None,
        export_transactions=transactions_output_file is not None,
        export_receipts=receipts_output_file is not None,
        export_logs=logs_output_file is not None,
        export_token_transfers=token_transfers_output_file is not None,
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_blocks.json"),
        read_file(blocks_output_file),
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_transactions.json"),
        read_file(transactions_output_file),
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_receipts.json"),
        read_file(receipts_output_file),
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_logs.json"), read_file(logs_output_file)
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_token_transfers.json"),
        read_file(token_transfers_output_file),
    )
