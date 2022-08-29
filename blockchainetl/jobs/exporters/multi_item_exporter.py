# MIT License
#
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

from typing import List, Dict, Any

from blockchainetl.atomic_counter import AtomicCounter
from blockchainetl.jobs.exporters.buffered_item_exporter import BufferedItemExporter
from blockchainetl.exporters import CsvItemExporter, JsonLinesItemExporter
from blockchainetl.file_utils import get_file_handle, close_silently

class MultifileItemExporter:
    def __init__(self, dirname_mapping, field_mapping=None, **kwargs):
        self.exporter_mapping: Dict[str, BufferedItemExporter] = {}
        self.counter_mapping: List[str, AtomicCounter] = {}

        self.dirname_mapping:Dict[str, str] = dirname_mapping
        self.field_mapping: Dict[str, List[str]] = field_mapping or {}

        self.exporter_options = kwargs
        self.logger = logging.getLogger('MultifileItemExporter')

    def open(self):
        for item_type, dirname in self.dirname_mapping.items():
            fields = self.field_mapping.get(item_type)
            self.exporter_mapping[item_type] = BufferedItemExporter(
                dirname=dirname, fields=fields, **self.exporter_options) if dirname is not None else None
            self.counter_mapping[item_type] = AtomicCounter()

    def export_items(self, items):
        for item in items:
            self.export_item(item)

    def export_item(self, item):
        item_type = item.get('type', None)
        if item_type is None:
            raise ValueError('"type" key is not found in item {}'.format(repr(item)))

        # get buffer and append item
        exporter = self.exporter_mapping.get(item_type)
        if exporter is None:
            raise ValueError(
                'Exporter for item type {} not found'.format(item_type))
        exporter.export_item(item)

        # counter: increment and get
        counter = self.counter_mapping.get(item_type)
        if counter is not None:
            counter.increment()


    def close(self):
        for item_type, exporter in self.exporter_mapping.items():
            if exporter is not None:
                exporter.close()
            counter = self.counter_mapping.get(item_type)
            if counter is not None:
                self.logger.info('{} items exported: {}'.format(item_type, counter.increment() - 1))
