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


import click

from klaytnetl.cli.export_all import export_all
from klaytnetl.cli.export_blocks_and_transactions import export_blocks_and_transactions

from klaytnetl.cli.export_block_group import export_block_group
from klaytnetl.cli.export_trace_group import export_trace_group

from klaytnetl.cli.export_contracts import export_contracts
from klaytnetl.cli.export_receipts_and_logs import export_receipts_and_logs
from klaytnetl.cli.export_token_transfers import export_token_transfers
from klaytnetl.cli.export_tokens import export_tokens
from klaytnetl.cli.export_traces import export_traces
from klaytnetl.cli.extract_contracts import extract_contracts
from klaytnetl.cli.extract_csv_column import extract_csv_column
from klaytnetl.cli.extract_field import extract_field
from klaytnetl.cli.extract_token_transfers import extract_token_transfers
from klaytnetl.cli.extract_tokens import extract_tokens
from klaytnetl.cli.filter_items import filter_items
from klaytnetl.cli.get_block_range_for_date import get_block_range_for_date
from klaytnetl.cli.get_block_range_for_timestamps import get_block_range_for_timestamps
from klaytnetl.cli.get_keccak_hash import get_keccak_hash


@click.group()
@click.version_option(version="0.3.0")
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(export_all, "export_all")
cli.add_command(export_blocks_and_transactions, "export_blocks_and_transactions")

cli.add_command(export_receipts_and_logs, "export_receipts_and_logs")
cli.add_command(export_token_transfers, "export_token_transfers")
cli.add_command(extract_token_transfers, "extract_token_transfers")
cli.add_command(export_contracts, "export_contracts")
cli.add_command(export_tokens, "export_tokens")
cli.add_command(export_traces, "export_traces")
cli.add_command(extract_contracts, "extract_contracts")
cli.add_command(extract_tokens, "extract_tokens")

cli.add_command(export_block_group, "export_block_group")
cli.add_command(export_trace_group, "export_trace_group")

# utils
cli.add_command(get_block_range_for_date, "get_block_range_for_date")
cli.add_command(get_block_range_for_timestamps, "get_block_range_for_timestamps")
cli.add_command(get_keccak_hash, "get_keccak_hash")
cli.add_command(extract_csv_column, "extract_csv_column")
cli.add_command(filter_items, "filter_items")
cli.add_command(extract_field, "extract_field")
