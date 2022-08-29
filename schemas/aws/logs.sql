CREATE EXTERNAL TABLE IF NOT EXISTS logs (
  log_index BIGINT,
  transaction_hash STRING,
  transaction_index BIGINT,
  address STRING,
  data STRING,
  topics ARRAY<STRING>,
  block_timestamp TIMESTAMP,
  transaction_receipt_status BIGINT,
  block_number BIGINT,
  block_unix_timestamp DOUBLE,
  block_hash STRING
)
PARTITIONED BY (block_date STRING)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://<your_bucket>/export/logs/';

MSCK REPAIR TABLE logs;