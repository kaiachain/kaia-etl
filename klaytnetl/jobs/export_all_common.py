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


import json
import logging
import os
from time import time

from web3 import Web3
from web3.middleware import geth_poa_middleware

from blockchainetl.file_utils import smart_open
from klaytnetl.jobs.export_blocks_job import ExportBlocksJob
from klaytnetl.jobs.export_contracts_job import ExportContractsJob
from klaytnetl.jobs.export_receipts_job import ExportReceiptsJob
from klaytnetl.jobs.export_token_transfers_job import ExportTokenTransfersJob
from klaytnetl.jobs.extract_tokens_job import ExtractTokensJob
from klaytnetl.jobs.exporters.blocks_and_transactions_item_exporter import (
    blocks_and_transactions_item_exporter,
)
from klaytnetl.jobs.exporters.contracts_item_exporter import contracts_item_exporter
from klaytnetl.jobs.exporters.receipts_and_logs_item_exporter import (
    receipts_and_logs_item_exporter,
)
from klaytnetl.jobs.exporters.token_transfers_item_exporter import (
    token_transfers_item_exporter,
)
from klaytnetl.jobs.exporters.tokens_item_exporter import tokens_item_exporter
from klaytnetl.providers.auto import get_provider_from_uri
from klaytnetl.thread_local_proxy import ThreadLocalProxy

logger = logging.getLogger("export_all")


def export_all_common(partitions, output_dir, provider_uri, max_workers, batch_size):

    for batch_start_block, batch_end_block, partition_dir in partitions:
        # # # start # # #
        start_time = time()

        padded_batch_start_block = str(batch_start_block).zfill(8)
        padded_batch_end_block = str(batch_end_block).zfill(8)
        block_range = "{padded_batch_start_block}-{padded_batch_end_block}".format(
            padded_batch_start_block=padded_batch_start_block,
            padded_batch_end_block=padded_batch_end_block,
        )
        file_name_suffix = "{padded_batch_start_block}_{padded_batch_end_block}".format(
            padded_batch_start_block=padded_batch_start_block,
            padded_batch_end_block=padded_batch_end_block,
        )

        # # # blocks_and_transactions # # #

        blocks_output_dir = "{output_dir}/blocks{partition_dir}".format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(blocks_output_dir), exist_ok=True)

        transactions_output_dir = "{output_dir}/transactions{partition_dir}".format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(transactions_output_dir), exist_ok=True)

        blocks_file = "{blocks_output_dir}/blocks_{file_name_suffix}.json".format(
            blocks_output_dir=blocks_output_dir,
            file_name_suffix=file_name_suffix,
        )
        transactions_file = (
            "{transactions_output_dir}/transactions_{file_name_suffix}.json".format(
                transactions_output_dir=transactions_output_dir,
                file_name_suffix=file_name_suffix,
            )
        )
        logger.info(
            "Exporting blocks {block_range} to {blocks_file}".format(
                block_range=block_range,
                blocks_file=blocks_file,
            )
        )
        logger.info(
            "Exporting transactions from blocks {block_range} to {transactions_file}".format(
                block_range=block_range,
                transactions_file=transactions_file,
            )
        )

        job = ExportBlocksJob(
            start_block=batch_start_block,
            end_block=batch_end_block,
            batch_size=batch_size,
            batch_web3_provider=ThreadLocalProxy(
                lambda: get_provider_from_uri(provider_uri, batch=True)
            ),
            max_workers=max_workers,
            item_exporter=blocks_and_transactions_item_exporter(
                blocks_file, transactions_file
            ),
            export_blocks=blocks_file is not None,
            export_transactions=transactions_file is not None,
        )
        job.run()

        # # # token_transfers # # #
        token_transfers_output_dir = (
            "{output_dir}/token_transfers{partition_dir}".format(
                output_dir=output_dir,
                partition_dir=partition_dir,
            )
        )
        os.makedirs(os.path.dirname(token_transfers_output_dir), exist_ok=True)

        token_transfers_file = "{token_transfers_output_dir}/token_transfers_{file_name_suffix}.json".format(
            token_transfers_output_dir=token_transfers_output_dir,
            file_name_suffix=file_name_suffix,
        )
        logger.info(
            "Exporting ERC20 transfers from blocks {block_range} to {token_transfers_file}".format(
                block_range=block_range,
                token_transfers_file=token_transfers_file,
            )
        )

        web3 = Web3(get_provider_from_uri(provider_uri))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        job = ExportTokenTransfersJob(
            start_block=batch_start_block,
            end_block=batch_end_block,
            batch_size=batch_size,
            web3=ThreadLocalProxy(lambda: web3),
            item_exporter=token_transfers_item_exporter(token_transfers_file),
            max_workers=max_workers,
        )
        job.run()

        # # # receipts_and_logs # # #
        receipts_output_dir = "{output_dir}/receipts{partition_dir}".format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(receipts_output_dir), exist_ok=True)

        logs_output_dir = "{output_dir}/logs{partition_dir}".format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(logs_output_dir), exist_ok=True)

        receipts_file = "{receipts_output_dir}/receipts_{file_name_suffix}.json".format(
            receipts_output_dir=receipts_output_dir,
            file_name_suffix=file_name_suffix,
        )
        logs_file = "{logs_output_dir}/logs_{file_name_suffix}.json".format(
            logs_output_dir=logs_output_dir,
            file_name_suffix=file_name_suffix,
        )
        logger.info(
            "Exporting receipts and logs from blocks {block_range} to {receipts_file} and {logs_file}".format(
                block_range=block_range,
                receipts_file=receipts_file,
                logs_file=logs_file,
            )
        )

        with smart_open(transactions_file, "r") as transaction_hashes:
            job = ExportReceiptsJob(
                transaction_hashes_iterable=(
                    json.loads(transaction)["hash"].strip()
                    for transaction in transaction_hashes
                ),
                batch_size=batch_size,
                batch_web3_provider=ThreadLocalProxy(
                    lambda: get_provider_from_uri(provider_uri, batch=True)
                ),
                max_workers=max_workers,
                item_exporter=receipts_and_logs_item_exporter(receipts_file, logs_file),
                export_receipts=receipts_file is not None,
                export_logs=logs_file is not None,
            )
            job.run()

        # # # contracts # # #
        contracts_output_dir = "{output_dir}/contracts{partition_dir}".format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(contracts_output_dir), exist_ok=True)

        contracts_file = (
            "{contracts_output_dir}/contracts_{file_name_suffix}.json".format(
                contracts_output_dir=contracts_output_dir,
                file_name_suffix=file_name_suffix,
            )
        )
        logger.info(
            "Exporting contracts from blocks {block_range} to {contracts_file}".format(
                block_range=block_range,
                contracts_file=contracts_file,
            )
        )

        with smart_open(receipts_file, "r") as receipts_file:
            contract_addresses = (
                {
                    "contract_address": json.loads(receipt)["contract_address"].strip(),
                    "block_number": json.loads(receipt)["block_number"],
                }
                for receipt in receipts_file
                if json.loads(receipt)["contract_address"] is not None
            )
            job = ExportContractsJob(
                contracts_iterable=contract_addresses,
                batch_size=batch_size,
                batch_web3_provider=ThreadLocalProxy(
                    lambda: get_provider_from_uri(provider_uri, batch=True)
                ),
                item_exporter=contracts_item_exporter(contracts_file),
                max_workers=max_workers,
            )
            job.run()

        # # # tokens # # #

        if token_transfers_file is not None:
            tokens_output_dir = "{output_dir}/tokens{partition_dir}".format(
                output_dir=output_dir,
                partition_dir=partition_dir,
            )
            os.makedirs(os.path.dirname(tokens_output_dir), exist_ok=True)

            tokens_file = "{tokens_output_dir}/tokens_{file_name_suffix}.json".format(
                tokens_output_dir=tokens_output_dir,
                file_name_suffix=file_name_suffix,
            )
            logger.info(
                "Exporting tokens from blocks {block_range} to {tokens_file}".format(
                    block_range=block_range,
                    tokens_file=tokens_file,
                )
            )

            web3 = Web3(get_provider_from_uri(provider_uri))
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)

            with smart_open(contracts_file, "r") as contracts_file:
                contracts_iterable = (json.loads(line) for line in contracts_file)
                job = ExtractTokensJob(
                    contracts_iterable=contracts_iterable,
                    web3=ThreadLocalProxy(lambda: web3),
                    item_exporter=tokens_item_exporter(tokens_file),
                    max_workers=max_workers,
                )

                job.run()

        # # # finish # # #
        end_time = time()
        time_diff = round(end_time - start_time, 5)
        logger.info(
            "Exporting blocks {block_range} took {time_diff} seconds".format(
                block_range=block_range,
                time_diff=time_diff,
            )
        )
