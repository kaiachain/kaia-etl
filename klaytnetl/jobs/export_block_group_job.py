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

from klaytnetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from klaytnetl.json_rpc_requests import (
    generate_get_block_with_receipt_by_number_json_rpc,
)

from klaytnetl.mappers.block_mapper import KlaytnBlockMapper
from klaytnetl.mappers.transaction_mapper import KlaytnTransactionMapper
from klaytnetl.mappers.receipt_mapper import KlaytnReceiptMapper
from klaytnetl.mappers.receipt_log_mapper import KlaytnReceiptLogMapper
from klaytnetl.mappers.token_transfer_mapper import KlaytnTokenTransferMapper
from klaytnetl.service.token_transfer_extractor import KlaytnTokenTransferExtractor

from klaytnetl.domain.block import KlaytnBlock

from klaytnetl.utils import rpc_response_batch_to_results, validate_range

from typing import List


# Exports blocks and transactions
class ExportBlockGroupJob(BaseJob):
    def __init__(
        self,
        start_block,
        end_block,
        batch_size,
        batch_web3_provider,
        max_workers,
        item_exporter,
        enrich=True,
        export_blocks=True,
        export_transactions=True,
        export_receipts=True,
        export_logs=True,
        export_token_transfers=True,
    ):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_web3_provider = batch_web3_provider

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.enrich = enrich

        # export options
        self.export_blocks = export_blocks
        self.export_transactions = export_transactions
        self.export_receipts = export_receipts
        self.export_logs = export_logs
        self.export_token_transfers = export_token_transfers

        # minimum condition for execution
        if (
            not self.export_blocks
            and not self.export_transactions
            and not self.export_receipts
            and not self.export_logs
            and not self.export_token_transfers
        ):
            raise ValueError(
                "At least one of export_blocks or export_transactions must be True"
            )

        # init mapper and construct dependency
        self._init_mapper(
            **{
                "export_blocks": self.export_blocks,
                "export_transactions": self.export_transactions,
                "export_receipts": self.export_receipts,
                "export_logs": self.export_logs,
                "export_token_transfers": self.export_token_transfers,
            }
        )

    def _init_mapper(
        self,
        export_blocks,
        export_transactions,
        export_receipts,
        export_logs,
        export_token_transfers,
    ):
        # mapper options
        self._require_block = True
        self._require_transaction = export_transactions
        self._require_receipt = export_receipts or export_logs or export_token_transfers
        self._require_receipt_log = export_logs or export_token_transfers
        self._require_token_transfer = export_token_transfers

        # init mapper
        self.block_mapper = (
            KlaytnBlockMapper(enrich=self.enrich) if self._require_block else None
        )
        self.transaction_mapper = (
            KlaytnTransactionMapper(enrich=self.enrich)
            if self._require_transaction
            else None
        )
        self.receipt_log_mapper = (
            KlaytnReceiptLogMapper(enrich=self.enrich)
            if self._require_receipt_log
            else None
        )
        self.receipt_mapper = (
            KlaytnReceiptMapper(enrich=self.enrich) if self._require_receipt else None
        )
        self.token_transfer_mapper = (
            KlaytnTokenTransferMapper(enrich=self.enrich)
            if self._require_token_transfer
            else None
        )
        self.token_transfer_extractor = (
            KlaytnTokenTransferExtractor(enrich=self.enrich)
            if self._require_token_transfer
            else None
        )

        # register mapper dependency
        if self.receipt_mapper is not None:
            self.receipt_mapper.register(receipt_log_mapper=self.receipt_log_mapper)
        self.block_mapper.register(
            transaction_mapper=self.transaction_mapper,
            receipt_mapper=self.receipt_mapper,
        )

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1,
        )

    def _export_batch(self, block_number_batch):
        blocks_rpc = list(
            generate_get_block_with_receipt_by_number_json_rpc(block_number_batch)
        )
        response = self.batch_web3_provider.make_batch_request(json.dumps(blocks_rpc))
        results = rpc_response_batch_to_results(response)
        blocks: List[KlaytnBlock] = [
            self.block_mapper.json_dict_to_block(result) for result in results
        ]

        for block in blocks:
            self._export_block(block)

    def _export_block(self, block):
        if self.export_blocks:
            self.item_exporter.export_item(self.block_mapper.block_to_dict(block))

        if self._require_transaction:
            for tx in block.transactions:
                if self.export_transactions:
                    self.item_exporter.export_item(
                        self.transaction_mapper.transaction_to_dict(tx)
                    )
        if self._require_receipt:
            for receipt in block.receipts:
                if self.export_receipts:
                    self.item_exporter.export_item(
                        self.receipt_mapper.receipt_to_dict(receipt)
                    )
                if self._require_receipt_log:
                    for log in receipt.logs:
                        if self.export_logs:
                            self.item_exporter.export_item(
                                self.receipt_log_mapper.receipt_log_to_dict(log)
                            )
                        if self.export_token_transfers:
                            token_transfer = (
                                self.token_transfer_extractor.extract_transfer_from_log(
                                    log
                                )
                            )
                            if token_transfer is not None:
                                self.item_exporter.export_item(
                                    self.token_transfer_mapper.token_transfer_to_dict(
                                        token_transfer
                                    )
                                )

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
