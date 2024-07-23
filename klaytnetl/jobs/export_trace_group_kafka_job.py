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
from klaytnetl.json_rpc_requests import generate_trace_block_by_number_json_rpc
from klaytnetl.json_rpc_requests import (
    generate_get_block_with_receipt_by_number_json_rpc,
)
from blockchainetl.jobs.base_job import BaseJob
from klaytnetl.mappers.trace_block_mapper import KlaytnTraceBlockMapper
from klaytnetl.mappers.trace_mapper import KlaytnTraceMapper
from klaytnetl.mappers.contract_mapper import KlaytnContractMapper
from klaytnetl.mappers.token_mapper import KlaytnTokenMapper

from klaytnetl.utils import (
    validate_range,
    rpc_response_to_result,
    rpc_response_batch_to_results,
)

from klaytnetl.domain.trace_block import KlaytnTraceBlock
from klaytnetl.domain.contract import KlaytnContract, KlaytnRawContract
from klaytnetl.domain.token import KlaytnToken, KlaytnRawToken

from klaytnetl.service.klaytn_contract_service import KlaytnContractService
from klaytnetl.service.klaytn_token_service import KlaytnTokenService

from klaytnetl.utils import hex_to_dec, is_contract_creation_trace


# Exports trace block
class ExportTraceGroupKafkaJob(BaseJob):
    def __init__(
        self,
        start_block,
        end_block,
        batch_size,
        batch_web3_provider,
        web3,
        max_workers,
        enrich,
        item_exporter,
        log_percentage_step=10,
        detailed_trace_log=False,
        export_traces=True,
        export_contracts=True,
        export_tokens=True,
    ):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_web3_provider = batch_web3_provider

        self.batch_work_executor = BatchWorkExecutor(
            batch_size, max_workers, log_percentage_step, detailed_trace_log
        )
        self.item_exporter = item_exporter

        self.export_traces = export_traces
        self.export_contracts = export_contracts
        self.export_tokens = export_tokens

        self.enrich = enrich

        if (
            not self.export_traces
            and not self.export_contracts
            and not self.export_tokens
        ):
            raise ValueError(
                "At least one of export_traces, export_contracts or export_tokens must be True"
            )

        self.web3 = web3

        self._init_mapper(
            **{
                "export_traces": self.export_traces,
                "export_contracts": self.export_contracts,
                "export_tokens": self.export_tokens,
            }
        )

    def _init_mapper(self, export_traces, export_contracts, export_tokens):
        # mapper options
        self._require_trace = True
        self._require_contract = export_contracts or export_tokens
        self._require_token = export_tokens

        # init mapper
        self.trace_block_mapper = (
            KlaytnTraceBlockMapper(enrich=self.enrich) if self._require_trace else None
        )
        self.trace_mapper = (
            KlaytnTraceMapper(enrich=self.enrich) if self._require_trace else None
        )

        self.contract_mapper = (
            KlaytnContractMapper(enrich=self.enrich) if self._require_contract else None
        )
        self.contract_service = (
            KlaytnContractService(self.web3) if self._require_contract else None
        )

        self.token_mapper = (
            KlaytnTokenMapper(enrich=self.enrich) if self._require_token else None
        )
        self.token_service = (
            KlaytnTokenService(self.web3, clean_user_provided_content)
            if self._require_token
            else None
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
        # export blocks and transactions
        blocks_rpc = list(
            generate_get_block_with_receipt_by_number_json_rpc(block_number_batch)
        )
        blocks_response = self.batch_web3_provider.make_batch_request(
            json.dumps(blocks_rpc)
        )
        blocks = filter(
            lambda blk: len(blk.get("transactions")) > 0,
            rpc_response_batch_to_results(blocks_response),
        )
        blocks = map(
            lambda blk: {
                "block_number": hex_to_dec(blk.get("number")),
                "block_hash": blk.get("hash"),
                "block_timestamp": hex_to_dec(blk.get("timestamp")) * 1.0
                + hex_to_dec(blk.get("timestampFoS")) * 0.001,
                "block_transactions": blk.get("transactions"),
            },
            blocks,
        )
        blocks_map = {}
        for block in blocks:
            blocks_map[block["block_number"]] = block

        # export trace blocks
        trace_blocks_rpc = list(
            generate_trace_block_by_number_json_rpc(block_number_batch)
        )

        # divide requests to small number of requests
        num = 0
        trace_blocks = []
        while num < len(trace_blocks_rpc):
            chunk = trace_blocks_rpc[num : num + 20]
            num = num + 20
            trace_blocks_response = self.batch_web3_provider.make_batch_request(
                json.dumps(chunk)
            )
            trace_blocks_chunk = map(
                lambda res: {
                    "block_number": res.get("id"),
                    "transaction_traces": [
                        tx_trace.get("result")
                        for tx_trace in rpc_response_to_result(res)
                    ],
                },
                trace_blocks_response,
            )
            trace_blocks_chunk = filter(
                lambda ntr: len(ntr.get("transaction_traces")) > 0, trace_blocks_chunk
            )
            trace_blocks.extend(trace_blocks_chunk)

        trace_count = 0
        for raw_trace_block in trace_blocks:
            block_number = raw_trace_block.get("block_number")
            block = blocks_map.get(block_number)
            trace_block: KlaytnTraceBlock = (
                self.trace_block_mapper.json_dict_to_trace_block(
                    raw_trace_block, **block
                )
            )

            for trace in self.trace_mapper.trace_block_to_trace(trace_block):
                trace_count += 1

                if self.export_traces:
                    self.item_exporter.export_item(
                        self.trace_mapper.trace_to_dict(trace)
                    )

                if self._require_contract and is_contract_creation_trace(trace):
                    if self.enrich:
                        contract = KlaytnContract.from_trace(
                            trace, self.contract_service
                        )
                    else:
                        contract = KlaytnRawContract.from_trace(
                            trace, self.contract_service
                        )

                    if self.export_contracts:
                        self.item_exporter.export_item(
                            self.contract_mapper.contract_to_dict(contract)
                        )

                    if self._require_token and (
                        contract.is_erc20 or contract.is_erc721 or contract.is_erc1155
                    ):
                        token_metadata = self.token_service.get_token_metadata(
                            contract.address
                        )
                        if self.enrich:
                            token = KlaytnToken.from_contract(
                                contract, **token_metadata
                            )
                        else:
                            token = KlaytnRawToken.from_contract(
                                contract, **token_metadata
                            )
                        if self.export_tokens:
                            self.item_exporter.export_item(
                                self.token_mapper.token_to_dict(token)
                            )
        return trace_count

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()


ASCII_0 = 0


def clean_user_provided_content(content):
    if isinstance(content, str):
        # This prevents this error in BigQuery
        # Error while reading data, error message: Error detected while parsing row starting at position: 9999.
        # Error: Bad character (ASCII 0) encountered.
        return content.translate({ASCII_0: None})
    else:
        return content
