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


from blockchainetl.jobs.exporters.singlefile_item_exporter import SinglefileItemExporter
from blockchainetl.jobs.exporters.multifile_item_exporter import MultifileItemExporter

BLOCK_FIELDS_TO_EXPORT = [
    "number",
    "hash",
    "parent_hash",
    "logs_bloom",
    "transactions_root",
    "state_root",
    "receipts_root",
    "size",
    "extra_data",
    # 'gas_limit',  # Does not supported by klay_getBlockWithConsensusInfoByNumber
    "gas_used",
    "block_timestamp",
    "block_unix_timestamp",
    "transaction_count",
    "block_score",
    "total_block_score",
    "governance_data",
    "vote_data",
    "committee",
    "proposer",
    "reward_address",
    "base_fee_per_gas",
]

TRANSACTION_FIELDS_TO_EXPORT = [
    "hash",
    "nonce",
    "block_hash",
    "block_number",
    "transaction_index",
    "from_address",
    "to_address",
    "value",
    "gas",
    "gas_price",
    "input",
    "fee_payer",
    "fee_payer_signatures",
    "fee_ratio",
    "sender_tx_hash",
    "signatures",
    "tx_type",
    "tx_type_int",
    "max_priority_fee_per_gas",
    "max_fee_per_gas",
    "access_list",
]

RECEIPT_FIELDS_TO_EXPORT = [
    "transaction_hash",
    "transaction_index",
    "block_hash",
    "block_number",
    "gas",
    "gas_price",
    "gas_used",
    "effective_gas_price",
    "contract_address",
    "logs_bloom",
    "nonce",
    "fee_payer",
    "fee_payer_signatures",
    "fee_ratio",
    "code_format",
    "human_readable",
    "tx_error",
    "key",
    "input_data",
    "from_address",
    "to_address",
    "type_name",
    "type_int",
    "sender_tx_hash",
    "signatures",
    "status",
    "value",
    "input_json",
    "access_list",
    "chain_id",
    "max_priority_fee_per_gas",
    "max_fee_per_gas",
]

LOG_FIELDS_TO_EXPORT = [
    "block_hash",
    "block_number",
    "transaction_hash",
    "transaction_index",
    "log_index",
    "address",
    "data",
    "topics",
]

TOKEN_TRANSFER_FIELDS_TO_EXPORT = [
    "token_address",
    "from_address",
    "to_address",
    "value",
    "block_hash",
    "block_number",
    "transaction_hash",
    "transaction_index",
    "log_index",
]


def raw_block_group_item_exporter(
    blocks_output=None,
    transactions_output=None,
    receipts_output=None,
    logs_output=None,
    token_transfers_output=None,
    **kwargs
):
    maxlines = kwargs.get("file_maxlines", None)

    if maxlines is None or maxlines <= 0:
        return SinglefileItemExporter(
            filename_mapping={
                "block": blocks_output,
                "transaction": transactions_output,
                "receipt": receipts_output,
                "log": logs_output,
                "token_transfer": token_transfers_output,
            },
            field_mapping={
                "block": BLOCK_FIELDS_TO_EXPORT,
                "transaction": TRANSACTION_FIELDS_TO_EXPORT,
                "receipt": RECEIPT_FIELDS_TO_EXPORT,
                "log": LOG_FIELDS_TO_EXPORT,
                "token_transfer": TOKEN_TRANSFER_FIELDS_TO_EXPORT,
            },
            **kwargs
        )
    else:
        return MultifileItemExporter(
            dirname_mapping={
                "block": blocks_output,
                "transaction": transactions_output,
                "receipt": receipts_output,
                "log": logs_output,
                "token_transfer": token_transfers_output,
            },
            field_mapping={
                "block": BLOCK_FIELDS_TO_EXPORT,
                "transaction": TRANSACTION_FIELDS_TO_EXPORT,
                "receipt": RECEIPT_FIELDS_TO_EXPORT,
                "log": LOG_FIELDS_TO_EXPORT,
                "token_transfer": TOKEN_TRANSFER_FIELDS_TO_EXPORT,
            },
            **kwargs
        )
