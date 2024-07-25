from typing import List


class Segment:
    def __init__(
        self,
        key: int,
        value: bytes,
        total_segments: int,
        segment_idx: int,
        producer_id: str,
    ):
        self.key = key  # block_number
        self.value = value
        self.total_segments = total_segments
        self.segment_idx = segment_idx
        self.producer_id = producer_id

    def __str__(self):
        return (
            f"Segment(key={self.key}, producer_id={self.producer_id},"
            f"segment_idx={self.segment_idx},"
            f"total_segments={self.total_segments})"
        )


class KafkaTrace:
    def __init__(
        self,
        block_number: int,
        trace: bytes,
        segments: List[Segment],
    ):
        self.block_number = block_number
        self.trace = trace
        self.segments = segments


def insert_segment(new_segment: Segment, buffer: List[List[Segment]]):
    for idx, buffered_segments in enumerate(buffer):
        num_buffered = len(buffered_segments)
        if (
            num_buffered > 0
            and buffered_segments[0].key == new_segment.key
            and buffered_segments[0].producer_id == new_segment.producer_id
        ):
            # there is a missing segment which should not exist.
            if new_segment.segment_idx > num_buffered:
                print(
                    f"[ERROR] there may be a missing segment "
                    f"[numBuffered: {num_buffered}, "
                    f"newSegment: {new_segment}]"
                )
                return buffer

            # the segment is already inserted to buffer.
            if new_segment.segment_idx < num_buffered:
                print(
                    f"[WARN] the message is duplicated " f"[newSegment: {new_segment}]"
                )
                return buffer

            # insert the segment to the buffer.
            buffer[idx].append(new_segment)
            return buffer

    if new_segment.segment_idx == 0:
        # create a segment slice and append it.
        buffer.append([new_segment])
    else:
        # the segment may be already handled.
        print(
            f"[WARN] the message may be inserted already. "
            f"drop the segment [segment: {new_segment}]"
        )

    return buffer


def handle_buffered_messages(buffer: List[List[Segment]]):
    complete_segments: List[KafkaTrace] = []
    while buffer:
        first_segment = buffer[0][0]
        if len(buffer[0]) != first_segment.total_segments:
            # first segment is not ready for assembling messages
            return complete_segments

        # ready for assembling message
        msg_buffer = bytearray()
        for segment in buffer[0]:
            msg_buffer.extend(segment.value)

        msg: KafkaTrace = KafkaTrace(first_segment.key, msg_buffer, buffer[0])

        complete_segments.append(msg)
        buffer.pop(0)

    return complete_segments
