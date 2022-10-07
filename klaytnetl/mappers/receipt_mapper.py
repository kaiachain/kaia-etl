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

from klaytnetl.domain.receipt import KlaytnRawReceipt, KlaytnReceipt

from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin
from klaytnetl.mappers.receipt_log_mapper import KlaytnReceiptLogMapper
from klaytnetl.utils import hex_to_dec, to_normalized_address

from typing import Union


class KlaytnReceiptMapper(BaseMapper, EnrichableMixin):
    def __init__(self, receipt_log_mapper=None, enrich=False):
        super(KlaytnReceiptMapper, self).__init__(enrich=enrich)
        self.receipt_log_mapper = receipt_log_mapper

    def register(self, receipt_log_mapper: KlaytnReceiptLogMapper = None) -> None:
        if receipt_log_mapper is not None and isinstance(
            receipt_log_mapper, KlaytnReceiptLogMapper
        ):
            if receipt_log_mapper.enrich != self.enrich:
                logging.warning(
                    "Enrich property for child_mapper doesn't match with"
                    " one for parent_mapper. It will force the value of parent_mapper."
                )
                receipt_log_mapper.enrich = self.enrich

            self.receipt_log_mapper = receipt_log_mapper

    def json_dict_to_receipt(self, json_dict, **kwargs) -> Union[KlaytnRawReceipt, KlaytnReceipt]:
        receipt = KlaytnRawReceipt()

        receipt.transaction_hash = json_dict.get("transactionHash")
        receipt.transaction_index = hex_to_dec(json_dict.get("transactionIndex"))
        receipt.block_hash = json_dict.get("blockHash")
        receipt.block_number = hex_to_dec(json_dict.get("blockNumber"))

        receipt.contract_address = to_normalized_address(
            json_dict.get("contractAddress")
        )
        receipt.status = hex_to_dec(json_dict.get("status"))

        receipt.gas = hex_to_dec(json_dict.get("gas"))
        receipt.gas_price = hex_to_dec(json_dict.get("gasPrice"))
        receipt.gas_used = hex_to_dec(json_dict.get("gasUsed"))
        receipt.effective_gas_price = hex_to_dec(json_dict.get("effectiveGasPrice"))

        receipt.logs_bloom = json_dict.get("logsBloom")
        receipt.nonce = hex_to_dec(json_dict.get("nonce"))
        receipt.fee_payer = json_dict.get("feePayer")
        receipt.fee_payer_signatures = json_dict.get("feePayerSignatures")
        receipt.fee_ratio = hex_to_dec(json_dict.get("feeRatio"))
        receipt.code_format = json_dict.get("codeFormat")
        receipt.human_readable = json_dict.get("humanReadable")
        receipt.tx_error = json_dict.get("txError")
        receipt.key = json_dict.get("key")
        receipt.input_data = json_dict.get("input")

        receipt.from_address = json_dict.get("from")
        receipt.to_address = json_dict.get("to")
        receipt.type_name = json_dict.get("type")
        receipt.type_int = json_dict.get("typeInt")

        receipt.sender_tx_hash = json_dict.get("senderTxHash")
        receipt.signatures = json_dict.get("signatures")
        receipt.value = hex_to_dec(json_dict.get("value"))

        receipt.input_json = json_dict.get("inputJSON")
        receipt.access_list = json_dict.get("accessList")
        receipt.chain_id = hex_to_dec(json_dict.get("chainId"))
        receipt.max_priority_fee_per_gas = hex_to_dec(
            json_dict.get("maxPriorityFeePerGas")
        )
        receipt.max_fee_per_gas = hex_to_dec(json_dict.get("maxFeePerGas"))

        if self.enrich:
            receipt = KlaytnReceipt.enrich(
                receipt,
                block_timestamp=kwargs.get("block_timestamp")
            )

        if self.receipt_log_mapper is not None and "logs" in json_dict:
            receipt.logs = [
                self.receipt_log_mapper.json_dict_to_receipt_log(
                    log,
                    block_timestamp=kwargs.get("block_timestamp"),
                    transaction_receipt_status=receipt.status,
                )
                for log in json_dict["logs"]
            ]

        return receipt

    def receipt_to_dict(self, receipt: Union[KlaytnRawReceipt, KlaytnReceipt]) -> dict:
        receipt_dict = {
            "type": "receipt",
            "transaction_hash": receipt.transaction_hash,
            "transaction_index": receipt.transaction_index,
            "block_hash": receipt.block_hash,
            "block_number": receipt.block_number,
            "contract_address": receipt.contract_address,
            "status": receipt.status,
            "gas": receipt.gas,
            "gas_price": receipt.gas_price,
            "gas_used": receipt.gas_used,
            "effective_gas_price": receipt.effective_gas_price,
            "logs_bloom": receipt.logs_bloom,
            "nonce": receipt.nonce,
            "fee_payer": receipt.fee_payer,
            "fee_payer_signatures": receipt.fee_payer_signatures,
            "fee_ratio": receipt.fee_ratio,
            "code_format": receipt.code_format,
            "human_readable": receipt.human_readable,
            "tx_error": receipt.tx_error,
            "key": receipt.key,
            "input_data": receipt.input_data,
            "from_address": receipt.from_address,
            "to_address": receipt.to_address,
            "type_name": receipt.type_name,
            "type_int": receipt.type_int,
            "sender_tx_hash": receipt.sender_tx_hash,
            "signatures": receipt.signatures,
            "value": receipt.value,
            "input_json": receipt.input_json,
            "access_list": receipt.access_list,
            "chain_id": receipt.chain_id,
            "max_priority_fee_per_gas": receipt.max_priority_fee_per_gas,
            "max_fee_per_gas": receipt.max_fee_per_gas,
        }

        if self.enrich and isinstance(receipt, KlaytnReceipt):
            receipt_dict["block_unix_timestamp"] = (
                receipt.block_timestamp.timestamp()
            )
            receipt_dict["block_timestamp"] = (
                receipt.block_timestamp.isoformat()
            )

        return receipt_dict
