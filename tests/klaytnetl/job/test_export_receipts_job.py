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
from klaytnetl.jobs.export_receipts_job import ExportReceiptsJob
from klaytnetl.jobs.exporters.receipts_and_logs_item_exporter import (
    receipts_and_logs_item_exporter,
)
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)

RESOURCE_GROUP = "test_export_receipts_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


DEFAULT_TX_HASHES = [
    "0x19613c8cf5a711cc3701dc5346ad095171150601abfcaf8e74ecbd536d4e4834",  # Account Update
    "0x090a5a01702402a09481eb7b3c5a895cbb67aa6a6bd2372c334cb8e7ce337571",  # Fee Delegated Account Update
    "0x19485bb473e7d90af7d3a67d6631f91f5abf6a6a1e24ff24a3dfe30c5028e168",  # Cancel
    "0x9b23a9ea174552fa158b41fab89be404b6b29aa5f24c2217e94625cf8a1c9a54",  # Fee Delegated Cancel
    "0x669a7671233a5d6bfe992c136a110196f2dbc367f76e508f4a425ffaee155324",  # Smart Contract Deploy
    "0x6c185414964f247fc9a0e9eb1e98d04887f3e1833721d303761f26087318c1ba",  # Fee Delegated Smart Contract Deploy
    "0xa8d369dd8aac128b08451a2c08ceda10d9735a8e53c8b3a01aa19df51eda5c79",  # Fee Delegated Smart Contract Deploy With Ratio
    "0xb93317dd74dd711b01a48debacb672e6c75bf000ee4e23831d85fce99eef576f",  # Smart Contract Execution
    "0x5eb066bd544519dd77657983d2daf67183bd9ad2c7c581978746d9a27f6a79f3",  # Fee Delegated Smart Contract Execution
    "0x5b665efa2da5a58da36af0e854734273247b4af3f38892412c07447ddde2a65a",  # Fee Delegated Smart Contract Execution With Ratio
    "0xb8fc58860ef41c54e72ba9a346232a952fbaf146244eae2cdce5f2c9063fb538",  # Legacy
    "0xbc22a4cd65003337d6bc70297df4401cab342e710f67769dc13999df92b34306",  # Chain Data Anchoring
    "0x5778fac21d744201bf0cce8c014207938f55eb9213989086f3f2228acbac4b54",  # Fee Delegated Chain Data Anchoring
    "0x16fe9780d7d159958425877870e0a9db3187392b2386b1e81463ae03b8d92512",  # Value Transfer
    "0xd6960970e0d741b37e2832d03ed4f6a935862fe9cea584e116ec3964205a654f",  # Fee Delegated Value Transfer
    "0x0d0cc98bb9460a70cb649c221e869d186b5b06048be750bc5a997c96d6d2071d",  # Fee Delegated Value Transfer With Ratio
    "0xa4d4c825506b9efaf59bc596c9547fc1a4587ef45bac0aed730ad718434130c6",  # Value Transfer Memo
    "0xf0b6f38c634ea5db75d736bac993681f71e77ade45ef4b7096d3ab941ec2ac2f",  # Fee Delegated Value Transfer Memo
    "0x50a7db8f2ac7564dd6ed0841728c5c43882b136c0130fa4b32989f5403d5e3e7",  # Fee Delegated Value Transfer Memo With Ratio
    "0x7975ee75e78d27c27f6bf4c1a5945272aa03ba19a67d0f7a89bcaeb20be61746",  # Ethereum Access List
    "0xc3e048276c600ed4034c1647326d5ab15ab231c8863ac878e33bc0d54f154375",  # Ethereum Dynamic Fee
    "0xf82a32f1b08265083061b5e52b2d3d93dcd726c9c4ff8abde1f3831106f88ec9",  # Failed
]


@pytest.mark.parametrize(
    "batch_size,transaction_hashes,output_format,resource_group,web3_provider_type",
    [
        (1, DEFAULT_TX_HASHES, "json", "receipts", "mock"),
        (2, DEFAULT_TX_HASHES, "json", "receipts", "mock"),
        skip_if_slow_tests_disabled(
            (2, DEFAULT_TX_HASHES, "json", "receipts", "fantrie")
        )
        # fantrie test will work once fantrie updates
    ],
)
def test_export_receipts_job(
    tmpdir,
    batch_size,
    transaction_hashes,
    output_format,
    resource_group,
    web3_provider_type,
):
    receipts_output_file = str(tmpdir.join("actual_receipts." + output_format))
    logs_output_file = str(tmpdir.join("actual_logs." + output_format))

    job = ExportReceiptsJob(
        transaction_hashes_iterable=transaction_hashes,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(
                web3_provider_type,
                lambda file: read_resource(resource_group, file),
                batch=True,
            )
        ),
        max_workers=5,
        item_exporter=receipts_and_logs_item_exporter(
            receipts_output_file, logs_output_file
        ),
        export_receipts=receipts_output_file is not None,
        export_logs=logs_output_file is not None,
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_receipts." + output_format),
        read_file(receipts_output_file),
    )

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_logs." + output_format),
        read_file(logs_output_file),
    )
