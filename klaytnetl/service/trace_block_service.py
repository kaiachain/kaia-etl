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


from typing import Iterable

from klaytnetl.utils import is_empty_trace_result

logger = logging.getLogger("trace_block_service")


def iterate_transaction_traces(
    transaction_traces: list, block_transactions: list = None
) -> Iterable:
    if block_transactions is not None:
        assert len(transaction_traces) == len(
            block_transactions
        ), "ValueError: transaction_traces and block_transactions must have same cardinality."
    else:
        logger.warn(
            "ValueWarn: A block_transactions field was not provided. The result will be with not enough information."
        )

    for idx, trace in enumerate(transaction_traces):
        if trace is None or is_empty_trace_result(trace):
            if block_transactions is not None:
                yield block_transactions[idx]
            else:
                yield None
        else:
            if block_transactions is not None:
                trace["transactionHash"] = block_transactions[idx].get(
                    "transactionHash"
                )
                trace["transactionIndex"] = block_transactions[idx].get(
                    "transactionIndex"
                )
                trace["transactionReceiptStatus"] = block_transactions[idx].get(
                    "status"
                )
            yield trace
