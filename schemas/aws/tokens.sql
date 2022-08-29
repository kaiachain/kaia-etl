CREATE EXTERNAL TABLE IF NOT EXISTS tokens (
  address STRING,
  symbol STRING,
  name STRING,
  decimals BIGINT,
  total_supply DECIMAL(38, 0),
  block_number BIGINT,
  block_hash STRING,
  function_sighashes ARRAY<STRING>,
  is_erc20 boolean,
  is_erc721 boolean,
  block_unix_timestamp DOUBLE,
  block_timestamp TIMESTAMP,
  transaction_hash STRING,
  transaction_index BIGINT,
  transaction_receipt_status BIGINT,
  trace_index BIGINT,
  trace_status BIGINT,
  creator_address STRING
)
PARTITIONED BY (block_date STRING)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://<your_bucket>/export/tokens/';

MSCK REPAIR TABLE tokens;