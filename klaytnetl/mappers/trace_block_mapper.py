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


from klaytnetl.domain.trace_block import KlaytnRawTraceBlock, KlaytnTraceBlock
from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin
from klaytnetl.service.trace_block_service import iterate_transaction_traces

from typing import Union


class KlaytnTraceBlockMapper(BaseMapper, EnrichableMixin):
    def __init__(self, enrich):
        super(KlaytnTraceBlockMapper, self).__init__(enrich=enrich)

    def json_dict_to_trace_block(
        self, json_dict, **kwargs
    ) -> Union[KlaytnRawTraceBlock, KlaytnTraceBlock]:
        _trace_block = KlaytnRawTraceBlock()

        _trace_block.block_number = json_dict.get("block_number")
        _trace_block.transaction_traces = list(
            iterate_transaction_traces(
                transaction_traces=json_dict.get("transaction_traces"),
                block_transactions=kwargs.get("block_transactions"),
            )
        )

        return (
            _trace_block
            if not self.enrich
            else KlaytnTraceBlock.enrich(
                raw_trace_block=_trace_block,
                block_hash=kwargs.get("block_hash"),
                block_timestamp=kwargs.get("block_timestamp"),
            )
        )

    def trace_block_to_dict(
        self,
        trace_block: Union[KlaytnRawTraceBlock, KlaytnTraceBlock],
        serializable=True,
    ) -> dict:
        trace_block_dict = {
            "type": "trace_block",
            "block_number": trace_block.block_number,
            "transaction_traces": trace_block.transaction_traces,
        }

        if self.enrich and isinstance(trace_block, KlaytnTraceBlock):
            trace_block_dict["block_hash"] = trace_block.block_hash
            trace_block_dict["block_timestamp"] = (
                trace_block.block_timestamp.isoformat()
                if serializable
                else trace_block.block_timestamp
            )
            trace_block_dict[
                "block_unix_timestamp"
            ] = trace_block.block_timestamp.timestamp()

        return trace_block_dict
