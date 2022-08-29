CREATE EXTERNAL TABLE IF NOT EXISTS token_transfers (
  token_address STRING,
  from_address STRING,
  to_address STRING,
  value DECIMAL(38, 0),
  transaction_hash STRING,
  transaction_index BIGINT,
  log_index BIGINT,
  block_timestamp TIMESTAMP,
  block_unix_timestamp DOUBLE,
  transaction_receipt_status BIGINT,
  block_number BIGINT,
  block_hash STRING
)
PARTITIONED BY (block_date STRING)
ROW FORMAT SERDE ''org.apache.hive.hcatalog.data.JsonSerDe''
LOCATION ''s3://<your_bucket>/export/token_transfers/'';

MSCK
REPAIR TABLE token_transfers;