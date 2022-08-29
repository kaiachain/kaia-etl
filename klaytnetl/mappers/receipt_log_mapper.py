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


from klaytnetl.domain.receipt_log import KlaytnReceiptLog, KlaytnRawReceiptLog
from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin
from klaytnetl.utils import hex_to_dec

from datetime import datetime
from typing import Union


class KlaytnReceiptLogMapper(BaseMapper, EnrichableMixin):
    def __init__(self, enrich=False):
        super(KlaytnReceiptLogMapper, self).__init__(enrich=enrich)

    def register(self):
        pass

    def json_dict_to_receipt_log(
        self, json_dict, **kwargs
    ) -> Union[KlaytnRawReceiptLog, KlaytnReceiptLog]:
        _receipt_log = KlaytnRawReceiptLog()

        _receipt_log.log_index = hex_to_dec(json_dict.get("logIndex"))
        _receipt_log.transaction_hash = json_dict.get("transactionHash")
        _receipt_log.transaction_index = hex_to_dec(json_dict.get("transactionIndex"))

        _receipt_log.block_hash = json_dict.get("blockHash")
        _receipt_log.block_number = hex_to_dec(json_dict.get("blockNumber"))

        _receipt_log.address = json_dict.get("address")
        _receipt_log.data = json_dict.get("data")
        _receipt_log.topics = json_dict.get("topics")
        _receipt_log.removed = json_dict.get("removed")

        return (
            _receipt_log
            if not self.enrich
            else KlaytnReceiptLog.enrich(
                _receipt_log,
                block_timestamp=kwargs.get("block_timestamp"),
                transaction_receipt_status=kwargs.get("transaction_receipt_status"),
            )
        )

    def receipt_log_to_dict(
        self,
        receipt_log: Union[KlaytnRawReceiptLog, KlaytnReceiptLog],
        serializable=True,
    ) -> dict:
        log_dict = {
            "type": "log",
            "log_index": receipt_log.log_index,
            "transaction_hash": receipt_log.transaction_hash,
            "transaction_index": receipt_log.transaction_index,
            "block_hash": receipt_log.block_hash,
            "block_number": receipt_log.block_number,
            "address": receipt_log.address,
            "data": receipt_log.data,
            "topics": receipt_log.topics,
            "removed": receipt_log.removed,
        }

        if self.enrich and isinstance(receipt_log, KlaytnReceiptLog):
            log_dict["block_timestamp"] = (
                receipt_log.block_timestamp.isoformat()
                if serializable
                else receipt_log.block_timestamp
            )
            log_dict["block_unix_timestamp"] = receipt_log.block_timestamp.timestamp()
            log_dict[
                "transaction_receipt_status"
            ] = receipt_log.transaction_receipt_status

        return log_dict

    def web3_dict_to_receipt_log(
        self, dict
    ) -> Union[KlaytnRawReceiptLog, KlaytnReceiptLog]:
        _receipt_log = KlaytnRawReceiptLog()

        _receipt_log.log_index = dict.get("logIndex")

        transaction_hash = dict.get("transactionHash")
        if transaction_hash is not None:
            transaction_hash = transaction_hash.hex()
        _receipt_log.transaction_hash = transaction_hash

        _receipt_log.transaction_index = dict.get("transactionIndex")

        block_hash = dict.get("blockHash")
        if block_hash is not None:
            block_hash = block_hash.hex()
        _receipt_log.block_hash = block_hash

        _receipt_log.block_number = dict.get("blockNumber")
        _receipt_log.address = dict.get("address")
        _receipt_log.data = dict.get("data")

        if "topics" in dict:
            _receipt_log.topics = [topic.hex() for topic in dict["topics"]]

        # raw or enrich
        if not self.enrich:
            return _receipt_log
        else:
            log = KlaytnReceiptLog()

            for k, v in _receipt_log.__dict__.items():
                if hasattr(log, k):
                    log.__setattr__(k, v)

            _block_timestamp: Union[datetime, str] = dict.get("block_timestamp")
            if isinstance(_block_timestamp, str):
                _block_timestamp = datetime.strptime(
                    _block_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            log.block_timestamp = _block_timestamp
            log.transaction_receipt_status = dict.get("transaction_receipt_status")

            return log

    def dict_to_receipt_log(self, dict) -> Union[KlaytnRawReceiptLog, KlaytnReceiptLog]:
        _receipt_log = KlaytnRawReceiptLog()

        _receipt_log.log_index = dict.get("log_index")
        _receipt_log.transaction_hash = dict.get("transaction_hash")
        _receipt_log.transaction_index = dict.get("transaction_index")
        _receipt_log.block_hash = dict.get("block_hash")
        _receipt_log.block_number = dict.get("block_number")
        _receipt_log.address = dict.get("address")
        _receipt_log.data = dict.get("data")
        _receipt_log.removed = dict.get("removed")

        # set topics
        topics = dict.get("topics")
        if isinstance(topics, str):
            if len(topics.strip()) == 0:
                _receipt_log.topics = []
            else:
                _receipt_log.topics = topics.strip().split(",")
        else:
            _receipt_log.topics = topics

        # raw or enrich
        if not self.enrich:
            return _receipt_log
        else:
            log = KlaytnReceiptLog()

            for k, v in _receipt_log.__dict__.items():
                if hasattr(log, k):
                    log.__setattr__(k, v)

            _block_timestamp: Union[datetime, str] = dict.get("block_timestamp")
            if isinstance(_block_timestamp, str):
                _block_timestamp = datetime.strptime(
                    _block_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            log.block_timestamp = _block_timestamp
            log.transaction_receipt_status = dict.get("transaction_receipt_status")

            return log
