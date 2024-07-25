from confluent_kafka import Producer

def read_file_and_send_to_kafka(testdata_path, kafka_topic, kafka_servers):
    producer = Producer({'bootstrap.servers': ','.join(kafka_servers)})
    
    def delivery_report(err, msg):
        if err is not None:
            raise Exception(f"Message delivery failed: {err}")

    with open(testdata_path, 'r') as file:
        for line in file:
            producer.produce(kafka_topic, line.encode('utf-8'), callback=delivery_report)
            producer.poll(0)
    
    producer.flush()

def main():
    for i in range(154474144, 154474164+1):
        testdata_path = f"testdata_{i}.json"
        kafka_topic = "local.klaytn.chaindatafetcher.en-0.tracegroup.v1"
        kafka_servers = ["localhost:9092"]
        read_file_and_send_to_kafka(testdata_path, kafka_topic, kafka_servers)
        print(f"Sent {testdata_path} to {kafka_topic}")

if __name__ == "__main__":
    main()
