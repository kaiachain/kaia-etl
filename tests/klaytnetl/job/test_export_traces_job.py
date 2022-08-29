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
from klaytnetl.jobs.exporters.raw_traces_item_exporter import raw_traces_item_exporter
from klaytnetl.jobs.exporters.enrich_traces_item_exporter import (
    enrich_traces_item_exporter,
)
from klaytnetl.jobs.export_traces_job import ExportTracesJob
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)

RESOURCE_GROUP = "test_export_traces_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "start_block,end_block,resource_group,enrich,web3_provider_type",
    [
        (1, 1, "block_without_transactions", True, "mock"),
        (99191493, 99191493, "block_with_create", True, "mock"),
        (87851605, 87851605, "block_with_suicide", True, "mock"),
        (99201113, 99201113, "block_with_subtraces", True, "mock"),
        (67972212, 67972212, "block_with_error", True, "mock"),
        skip_if_slow_tests_disabled(
            (99201113, 99201113, "block_with_subtraces", True, "fantrie")
        ),
    ],
)
def test_export_traces_job(
    tmpdir, start_block, end_block, resource_group, enrich, web3_provider_type
):
    traces_output_file = str(tmpdir.join("actual_traces.json"))

    if enrich:
        exporter = enrich_traces_item_exporter(traces_output_file)
    else:
        exporter = raw_traces_item_exporter(traces_output_file)

    job = ExportTracesJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=1,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(
                web3_provider_type,
                lambda file: read_resource(resource_group, file),
                batch=True,
            )
        ),
        max_workers=5,
        enrich=enrich,
        item_exporter=exporter,
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_traces.json"),
        read_file(traces_output_file),
    )
