CREATE EXTERNAL TABLE IF NOT EXISTS parquet_token_transfers (
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
PARTITIONED BY (start_block BIGINT, end_block BIGINT)
STORED AS PARQUET
LOCATION 's3://<your_bucket>/klaytnetl/parquet/token_transfers';

MSCK REPAIR TABLE parquet_token_transfers;