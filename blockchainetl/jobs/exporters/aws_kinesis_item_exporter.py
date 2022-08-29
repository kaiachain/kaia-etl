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

import json
import logging

import boto3
from timeout_decorator import timeout_decorator


class AwsKinesisItemExporter:

    def __init__(self, item_type_to_topic_mapping, message_attributes=('item_id',)):
        self.item_type_to_topic_mapping = item_type_to_topic_mapping
        self.publisher = boto3.client('kinesis', region_name='ap-northeast-2')
        self.message_attributes = message_attributes

    def open(self):
        pass

    def export_items(self, items):
        try:
            self._export_items_with_timeout(items)            
        except timeout_decorator.TimeoutError as e:
            logging.info('Recreating AWS Kinesis publisher.')
            self.publisher = boto3.client('kinesis', region_name='ap-northeast-2')
            raise e
    
    def chunks(self, it, n):
        chunk = []
        for i in it:
            chunk.append(i)
            if len(chunk) >= n:
                yield chunk
                chunk = []
        if len(chunk) > 0:
            yield chunk

    @timeout_decorator.timeout(300)
    def _export_items_with_timeout(self, items):
        records_mapping = {}

        for item in items:
            item_type = item.get('type')
            if item_type is not None and item_type in self.item_type_to_topic_mapping:
                topic_path = self.item_type_to_topic_mapping.get(item_type)
                data = json.dumps(item).encode('utf-8')

            records_mapping[topic_path] = records_mapping.get(topic_path, [])
            records_mapping[topic_path].append(dict(
                Data=data,
                PartitionKey=item.get('item_id')
            ))

        for topic_path, records in records_mapping.items():
            # PutRecordBatch takes only 500 records per scall
            for records_chunk in self.chunks(records, 500):
                self.publisher.put_records(Records=records_chunk, StreamName=topic_path)

    def export_item(self, item):
        item_type = item.get('type')
        if item_type is not None and item_type in self.item_type_to_topic_mapping:
            topic_path = self.item_type_to_topic_mapping.get(item_type)
            data = json.dumps(item).encode('utf-8')

            message_future = self.publisher.put_record(StreamName=topic_path, Data=data, PartitionKey=item.get('item_id'))

            return message_future
        else:
            logging.warning('Topic for item type "{}" is not configured.'.format(item_type))

    def get_message_attributes(self, item):
        attributes = {}

        for attr_name in self.message_attributes:
            if item.get(attr_name) is not None:
                attributes[attr_name] = item.get(attr_name)

        return attributes

    def close(self):
        pass