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


from klaytnetl.progress_logger import ProgressLogger


class TraceProgressLogger(ProgressLogger):
    def __init__(self, trace_count=0, name="work", logger=None, log_percentage_step=10, log_item_step=5000):
        super().__init__(name, logger, log_percentage_step, log_item_step)
        self.trace_count = trace_count

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def track(self, item_count=1, trace_count=0):
        processed_items = self.counter.increment(item_count)
        processed_items_before = processed_items - item_count

        track_message = None

        if trace_count:
            self.trace_count += trace_count

        current_trace_count = self.trace_count
        if self.total_items is None:
            if int(processed_items_before / self.log_items_step) != int(
                    processed_items / self.log_items_step
            ):
                track_message = "{} items processed.".format(processed_items)
        else:
            percentage = processed_items * 100 / self.total_items
            percentage_before = processed_items_before * 100 / self.total_items
            if int(percentage_before / self.log_percentage_step) != int(
                    percentage / self.log_percentage_step
            ):
                track_message = "{} items processed. Block Progress is {}%, Trace Count is {}".format(
                    processed_items, int(percentage), current_trace_count
                ) + ("!!!" if int(percentage) > 100 else ".")
                self.trace_count = 0

        if track_message is not None:
            self.logger.info(track_message)
