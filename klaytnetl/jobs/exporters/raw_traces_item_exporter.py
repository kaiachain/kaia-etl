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


from blockchainetl.jobs.exporters.singlefile_item_exporter import SinglefileItemExporter
from blockchainetl.jobs.exporters.multifile_item_exporter import MultifileItemExporter

FIELDS_TO_EXPORT = [
    "block_number",
    "transaction_hash",
    "transaction_index",
    "from_address",
    "to_address",
    "value",
    "input",
    "output",
    "trace_type",
    "call_type",
    "gas",
    "gas_used",
    "subtraces",
    "trace_address",
    "error",
    "status",
    "trace_index",
]


def raw_traces_item_exporter(traces_output, **kwargs):
    maxlines = kwargs.get("file_maxlines", None)

    if maxlines is None or maxlines <= 0:
        return SinglefileItemExporter(
            filename_mapping={
                "trace": traces_output,
            },
            field_mapping={
                "trace": FIELDS_TO_EXPORT,
            },
            **kwargs
        )
    else:
        return MultifileItemExporter(
            dirname_mapping={
                "trace": traces_output,
            },
            field_mapping={
                "trace": FIELDS_TO_EXPORT,
            },
            **kwargs
        )
