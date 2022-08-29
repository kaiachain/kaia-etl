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


from klaytnetl.domain.trace import KlaytnRawTrace, KlaytnTrace
from klaytnetl.domain.trace_block import KlaytnRawTraceBlock, KlaytnTraceBlock
from klaytnetl.mappers.base import BaseMapper
from klaytnetl.mixin.enrichable_mixin import EnrichableMixin
from klaytnetl.utils import hex_to_dec, to_normalized_address

from typing import Union, List, Tuple


class KlaytnTraceMapper(BaseMapper, EnrichableMixin):
    def __init__(self, enrich=True):
        super(KlaytnTraceMapper, self).__init__(enrich=enrich)

    def trace_block_to_trace(
        self, trace_block: Union[KlaytnTraceBlock, KlaytnRawTraceBlock]
    ) -> Union[List[KlaytnTrace], List[KlaytnRawTrace]]:
        block_number = trace_block.block_number
        transaction_traces = trace_block.transaction_traces

        traces: List[Union[KlaytnRawTrace, KlaytnTrace]] = []
        counter = -1

        for tx_index, tx_trace in enumerate(transaction_traces):
            rst, ctr = self._iterate_transaction_trace(
                block_number=block_number,
                tx_index=tx_index,
                tx_hash=tx_trace.get("transactionHash"),
                tx_status=hex_to_dec(tx_trace.get("transactionReceiptStatus")),
                tx_trace=tx_trace,
                parent_status=1,
                counter=counter + 1,
                trace_address=[],
                block_hash=trace_block.block_hash
                if isinstance(trace_block, KlaytnTraceBlock)
                else None,
                block_timestamp=trace_block.block_timestamp
                if isinstance(trace_block, KlaytnTraceBlock)
                else None,
            )
            counter = ctr
            traces.extend(rst)

        return traces

    def _iterate_transaction_trace(
        self,
        block_number,
        tx_index,
        tx_hash,
        tx_status,
        tx_trace,
        parent_status,
        counter,
        trace_address=[],
        **kwargs
    ) -> Union[Tuple[List[KlaytnTrace], int], Tuple[List[KlaytnRawTrace], int]]:
        trace = KlaytnRawTrace()
        trace.block_number = block_number

        trace.transaction_index = tx_index
        trace.transaction_hash = tx_hash

        trace.trace_index = counter

        trace.from_address = to_normalized_address(tx_trace.get("from"))
        trace.to_address = to_normalized_address(tx_trace.get("to"))

        trace.input = tx_trace.get("input", "0x")
        trace.output = tx_trace.get("output", "0x")

        trace.value = hex_to_dec(tx_trace.get("value"))
        trace.gas = hex_to_dec(tx_trace.get("gas"))
        trace.gas_used = hex_to_dec(tx_trace.get("gasUsed"))

        trace.error = tx_trace.get("error")

        trace.status = (
            tx_status
            * parent_status
            * (
                1
                if tx_trace.get("error") is None or len(tx_trace.get("error")) <= 0
                else 0
            )
        )

        # lowercase for compatibility with traces
        trace.trace_type = tx_trace.get("type").lower()
        if trace.trace_type == "selfdestruct":
            # rename to suicide for compatibility with traces
            trace.trace_type = "suicide"
        elif trace.trace_type in ("call", "callcode", "delegatecall", "staticcall"):
            trace.call_type = trace.trace_type
            trace.trace_type = "call"

        calls = tx_trace.get("calls", [])

        trace.subtraces = len(calls)
        trace.trace_address = trace_address

        result = [
            trace
            if not self.enrich
            else KlaytnTrace.enrich(
                trace,
                block_hash=kwargs.get("block_hash"),
                block_timestamp=kwargs.get("block_timestamp"),
                transaction_receipt_status=tx_status,
            )
        ]

        for call_index, call_trace in enumerate(calls):
            rst, ctr = self._iterate_transaction_trace(
                block_number=block_number,
                tx_index=tx_index,
                tx_hash=tx_hash,
                tx_status=tx_status,
                tx_trace=call_trace,
                parent_status=trace.status,
                counter=counter + 1,
                trace_address=trace_address + [call_index],
                **kwargs
            )

            counter = ctr
            result.extend(rst)

        return result, counter

    def trace_to_dict(
        self, trace: Union[KlaytnRawTrace, KlaytnTrace], serializable=True
    ) -> dict:
        trace_dict = {
            "type": "trace",
            "block_number": trace.block_number,
            "transaction_hash": trace.transaction_hash,
            "transaction_index": trace.transaction_index,
            "trace_index": trace.trace_index,
            "from_address": trace.from_address,
            "to_address": trace.to_address,
            "value": int(trace.value) if serializable else trace.value,
            "input": trace.input,
            "output": trace.output,
            "trace_type": trace.trace_type,
            "call_type": trace.call_type,
            "gas": trace.gas,
            "gas_used": trace.gas_used,
            "subtraces": trace.subtraces,
            "trace_address": trace.trace_address,
            "error": trace.error,
            "status": trace.status,
        }

        if self.enrich and isinstance(trace, KlaytnTrace):
            trace_dict["block_hash"] = trace.block_hash
            trace_dict["block_timestamp"] = (
                trace.block_timestamp.isoformat()
                if serializable
                else trace.block_timestamp
            )
            trace_dict["block_unix_timestamp"] = trace.block_timestamp.timestamp()
            trace_dict["transaction_receipt_status"] = trace.transaction_receipt_status

        return trace_dict
