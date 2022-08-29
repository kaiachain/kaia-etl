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


from klaytnetl.domain.token_transfer import KlaytnRawTokenTransfer, KlaytnTokenTransfer
from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin
from typing import Union


class KlaytnTokenTransferMapper(BaseMapper, EnrichableMixin):
    def __init__(self, enrich=False):
        super(KlaytnTokenTransferMapper, self).__init__(enrich=enrich)

    def register(self):
        pass

    def token_transfer_to_dict(
        self,
        token_transfer: Union[KlaytnRawTokenTransfer, KlaytnTokenTransfer],
        serializable=True,
    ):
        token_transfer_dict = {
            "type": "token_transfer",
            "token_address": token_transfer.token_address,
            "from_address": token_transfer.from_address,
            "to_address": token_transfer.to_address,
            "value": int(token_transfer.value)
            if serializable
            else token_transfer.value,
            "log_index": token_transfer.log_index,
            "transaction_hash": token_transfer.transaction_hash,
            "transaction_index": token_transfer.transaction_index,
            "block_hash": token_transfer.block_hash,
            "block_number": token_transfer.block_number,
        }

        if self.enrich and isinstance(token_transfer, KlaytnTokenTransfer):
            token_transfer_dict["block_timestamp"] = (
                token_transfer.block_timestamp.isoformat()
                if serializable
                else token_transfer.block_timestamp
            )
            token_transfer_dict[
                "block_unix_timestamp"
            ] = token_transfer.block_timestamp.timestamp()
            token_transfer_dict[
                "transaction_receipt_status"
            ] = token_transfer.transaction_receipt_status

        return token_transfer_dict
