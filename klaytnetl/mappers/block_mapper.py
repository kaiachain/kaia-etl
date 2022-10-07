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


import logging

from klaytnetl.domain.block import KlaytnBlock, KlaytnRawBlock

from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin
from klaytnetl.mappers.transaction_mapper import KlaytnTransactionMapper
from klaytnetl.mappers.receipt_mapper import KlaytnReceiptMapper
from klaytnetl.utils import hex_to_dec, is_full_block

from typing import Union


class KlaytnBlockMapper(BaseMapper, EnrichableMixin):
    def __init__(
        self,
        transaction_mapper: KlaytnTransactionMapper = None,
        receipt_mapper: KlaytnReceiptMapper = None,
        enrich: bool = False,
    ):
        super(KlaytnBlockMapper, self).__init__(enrich=enrich)

        self.transaction_mapper = transaction_mapper
        self.receipt_mapper = receipt_mapper

    def register(
        self,
        transaction_mapper: KlaytnTransactionMapper = None,
        receipt_mapper: KlaytnReceiptMapper = None,
    ) -> None:

        if transaction_mapper is not None and isinstance(
            transaction_mapper, KlaytnTransactionMapper
        ):
            if self.enrich != transaction_mapper.enrich:
                logging.warning(
                    "Enrich property for child_mapper doesn't match with one for parent_mapper. "
                    "It will force the value of parent_mapper."
                )
                transaction_mapper.enrich = self.enrich

            self.transaction_mapper = transaction_mapper

        if receipt_mapper is not None and isinstance(
            receipt_mapper, KlaytnReceiptMapper
        ):
            if self.enrich != receipt_mapper.enrich:
                logging.warning(
                    "Enrich property for child_mapper doesn't match with one for parent_mapper. "
                    "It will force the value of parent_mapper."
                )
                receipt_mapper.enrich = self.enrich

            self.receipt_mapper = receipt_mapper

    def json_dict_to_block(self, json_dict) -> Union[KlaytnRawBlock, KlaytnBlock]:
        _block = KlaytnRawBlock()
        _block.number = hex_to_dec(json_dict.get("number"))
        _block.hash = json_dict.get("hash")
        _block.parent_hash = json_dict.get("parentHash")
        _block.logs_bloom = json_dict.get("logsBloom")
        _block.transactions_root = json_dict.get("transactionsRoot")
        _block.state_root = json_dict.get("stateRoot")
        _block.receipts_root = json_dict.get("receiptsRoot")

        _block.size = hex_to_dec(json_dict.get("size"))
        _block.extra_data = json_dict.get("extraData")
        _block.gas_used = hex_to_dec(json_dict.get("gasUsed"))

        _block.timestamp = (
            hex_to_dec(json_dict.get("timestamp")) * 1.0
            + hex_to_dec(json_dict.get("timestampFoS")) * 0.001
        )

        # Klaytn additional properties
        _block.block_score = hex_to_dec(json_dict.get("blockscore"))
        _block.total_block_score = hex_to_dec(json_dict.get("totalBlockScore"))

        _block.governance_data = json_dict.get("governanceData")
        _block.vote_data = json_dict.get("voteData")

        _block.committee = json_dict.get("committee")
        _block.proposer = json_dict.get("proposer")
        _block.reward_address = json_dict.get("reward")

        _block.base_fee_per_gas = hex_to_dec(json_dict.get("baseFeePerGas"))

        # transactions or receipts
        _transactions = json_dict.get("transactions", [])

        _block.transaction_count = len(_transactions)

        if self.transaction_mapper is not None:
            _block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(
                    tx, block_timestamp=_block.timestamp
                )
                for tx in _transactions
                if isinstance(tx, dict)  # if not, transaction has no detail info
            ]

        if self.receipt_mapper is not None and is_full_block(json_dict):
            _block.receipts = [
                self.receipt_mapper.json_dict_to_receipt(
                    tx, block_timestamp=_block.timestamp
                )
                for tx in _transactions
                if isinstance(tx, dict) and "logs" in tx
            ]

        return _block if not self.enrich else KlaytnBlock.enrich(_block)

    def block_to_dict(
        self, block: Union[KlaytnBlock, KlaytnRawBlock], serializable=True
    ) -> dict:
        block_dict = {
            "type": "block",
            "number": block.number,
            "hash": block.hash,
            "parent_hash": block.parent_hash,
            "logs_bloom": block.logs_bloom,
            "transactions_root": block.transactions_root,
            "state_root": block.state_root,
            "receipts_root": block.receipts_root,
            "size": block.size,
            "extra_data": block.extra_data,
            "gas_used": int(block.gas_used) if serializable else block.gas_used,
            "block_timestamp": block.timestamp.isoformat()
            if serializable
            else block.timestamp,
            "block_unix_timestamp": block.timestamp.timestamp(),
            "transaction_count": block.transaction_count,
            # Klaytn additional properties
            "block_score": block.block_score,
            "total_block_score": block.total_block_score,
            "governance_data": block.governance_data,
            "vote_data": block.vote_data,
            "committee": block.committee,
            "proposer": block.proposer,
            "reward_address": block.reward_address,
            "base_fee_per_gas": block.base_fee_per_gas,
        }

        return block_dict
