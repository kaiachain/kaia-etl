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


from klaytnetl.domain.token import KlaytnRawToken, KlaytnToken
from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin

from typing import Union


class KlaytnTokenMapper(BaseMapper, EnrichableMixin):
    def __init__(self, enrich: bool = False):
        super(KlaytnTokenMapper, self).__init__(enrich=enrich)

    def token_to_dict(
        self, token: Union[KlaytnRawToken, KlaytnToken], serializable=True
    ) -> dict:
        token_dict: dict = {
            "type": "token",
            "address": token.address,
            "symbol": token.symbol,
            "name": token.name,
            "decimals": token.decimals,
            "total_supply": int(token.total_supply)
            if serializable and token.total_supply is not None
            else token.total_supply,
            "block_number": token.block_number,
        }
        if self.enrich and isinstance(token, KlaytnToken):
            token_dict["function_sighashes"] = token.function_sighashes
            token_dict["is_erc20"] = token.is_erc20
            token_dict["is_erc721"] = token.is_erc721
            token_dict["is_erc1155"] = token.is_erc1155
            token_dict["block_hash"] = token.block_hash
            token_dict["block_unix_timestamp"] = token.block_timestamp.timestamp()
            token_dict["block_timestamp"] = (
                token.block_timestamp.isoformat()
                if serializable
                else token.block_timestamp
            )
            token_dict["transaction_hash"] = token.transaction_hash
            token_dict["transaction_index"] = token.transaction_index
            token_dict["transaction_receipt_status"] = token.transaction_receipt_status
            token_dict["trace_index"] = token.trace_index
            token_dict["trace_status"] = token.trace_status
            token_dict["creator_address"] = token.creator_address

        return token_dict
