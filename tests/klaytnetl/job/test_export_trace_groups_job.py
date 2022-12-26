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

from klaytnetl.web3_utils import build_web3

import tests.resources
from klaytnetl.jobs.export_trace_group_job import ExportTraceGroupJob
from klaytnetl.jobs.exporters.raw_trace_group_item_exporter import (
    raw_trace_group_item_exporter,
)
from klaytnetl.jobs.exporters.enrich_trace_group_item_exporter import (
    enrich_trace_group_item_exporter,
)
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)

RESOURCE_GROUP = "test_export_trace_groups_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "start_block,end_block,enrich,batch_size,resource_group,web3_provider_type",
    [
        # Will resume once debug issue is fixed
        # skip_if_slow_tests_disabled(
        #     (77934351, 77934351, True, 1, "trace_groups_enrich", "fantrie")
        # ),
        # skip_if_slow_tests_disabled(
        #     (77934351, 77934351, False, 1, "trace_groups_raw", "fantrie")
        # ),
    ],
)
def test_export_trace_groups_job(
    tmpdir,
    start_block,
    end_block,
    enrich,
    batch_size,
    resource_group,
    web3_provider_type,
):
    traces_output_file = str(tmpdir.join("actual_traces.json"))
    contracts_output_file = str(tmpdir.join("actual_contracts.json"))
    tokens_output_file = str(tmpdir.join("actual_tokens.json"))

    if enrich:
        exporter = enrich_trace_group_item_exporter(
            traces_output_file, contracts_output_file, tokens_output_file
        )
    else:
        exporter = raw_trace_group_item_exporter(
            traces_output_file, contracts_output_file, tokens_output_file
        )

    job = ExportTraceGroupJob(
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
        web3=ThreadLocalProxy(
            lambda: build_web3(
                get_web3_provider(
                    web3_provider_type, lambda file: read_resource(resource_group, file)
                )
            )
        ),
        max_workers=5,
        item_exporter=exporter,
        export_traces=traces_output_file,
        export_contracts=contracts_output_file,
        export_tokens=tokens_output_file,
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_traces.json"),
        read_file(traces_output_file),
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_contracts.json"),
        read_file(contracts_output_file),
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_tokens.json"),
        read_file(tokens_output_file),
    )
