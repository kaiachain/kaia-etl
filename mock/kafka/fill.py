from confluent_kafka import Producer
import json
import re
import os

def split(data: bytes, size: int):
    segments = []
    while len(data) > size:
        segments.append(data[:size])
        data = data[size:]
    segments.append(data)
    return segments, len(segments)
    
def make_producer_message(topic: str, key: str, segment: bytes, segment_idx: int, total_segments: int):
    headers = [
        ('totalSegments', total_segments.to_bytes(8, 'big')),
        ('segmentIdx', segment_idx.to_bytes(8, 'big')),
        ('version', "1.0"),
        ('producerId', 'mock-kafka-producer'),
    ]
    return {
        'topic': topic,
        'key': key.encode('utf-8') if key else None,
        'value': segment,
        'headers': headers
    }

def read_file_and_send_to_kafka(testdata_path: str, kafka_topic: str, kafka_servers: list[str]):
    producer = Producer({'bootstrap.servers': ','.join(kafka_servers)})

    def delivery_report(err, msg):
        if err is not None:
            raise Exception(f"Message delivery failed: {err}")

    with open(testdata_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            data_bytes = json.dumps(data).encode('utf-8')
            key = re.search(r'testdata_(\d+)\.json', testdata_path).group(1) # block number
            segments, total_segments = split(data_bytes, 500 * 1024)  # 1MB segments

            for idx, segment in enumerate(segments):
                assert len(segment) <= 1000 * 1000
                msg = make_producer_message(kafka_topic, key, segment, idx, total_segments)
                producer.produce(**msg, callback=delivery_report)
                producer.poll(0)
                print(f"Sent {key}[{idx}] to {kafka_topic}")
    
    producer.flush()

def main():
    kafka_topic = "local.klaytn.chaindatafetcher.en-0.tracegroup.v1"
    kafka_servers = ["localhost:9092"]

    for i in range(154474144, 154474164+1):
        testdata_path = f"testdata_{i}.json"
        read_file_and_send_to_kafka(testdata_path, kafka_topic, kafka_servers)

    longdata = "testdata_9999999999.json"
    if os.path.exists(longdata):
        read_file_and_send_to_kafka(longdata, kafka_topic, kafka_servers)

if __name__ == "__main__":
    main()
