# MIT License
#
# Copyright (c) 2018 Jettson Lim, jettson.lim@groundx.xyz
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

import os
import json

from typing import List, Union, Optional, Any
from collections import deque
from blockchainetl.atomic_counter import AtomicCounter
from blockchainetl.exporters import JsonLinesItemExporter, CsvItemExporter
from blockchainetl.file_utils import get_file_handle, close_silently


class BufferedItemExporter:
    def __init__(self, dirname, fields, file_format='json', file_maxlines=None, compress=False, **kwargs):
        self.item_buffer: deque = deque()
        self.counter: AtomicCounter = AtomicCounter()

        self.dirname: str = os.path.relpath(dirname)
        self.fields: List[str] = fields
        self.file_format: str = file_format
        self.file_maxlines: int = file_maxlines
        self.compress: bool = compress

    def export_item(self, item):
        self.item_buffer.append(item)

        # starts with 1, get increment by 1
        cnt = self.counter.increment()

        # export item if counter
        if cnt % self.file_maxlines == 0:
            filename = self._get_filename(counter=cnt)
            self._export_item(filename, file_maxlines=self.file_maxlines)

    def close(self):
        cnt = self.counter.increment() - 1
        filename = self._get_filename(counter=cnt)
        if len(self.item_buffer) > 0:
            self._export_item(filename, len(self.item_buffer))

    def _get_filename(self, counter):
        return os.path.join(self.dirname, os.path.relpath(f'data-{int((counter-1) / self.file_maxlines):012}.{self.file_format}{".gz" if self.compress else ""}'))

    def _export_item(self, filename, file_maxlines):
        file = get_file_handle(filename, binary=True, compress=self.compress)

        if self.file_format == 'json':
            item_exporter = JsonLinesItemExporter(file, fields_to_export=self.fields)
        else:
            item_exporter = CsvItemExporter(file, fields_to_export=self.fields)

        for _ in range(file_maxlines):
            item_exporter.export_item(self.item_buffer.popleft())

        close_silently(file)
