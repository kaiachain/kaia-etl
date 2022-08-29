CREATE EXTERNAL TABLE IF NOT EXISTS contracts (
  address STRING,
  bytecode STRING,
  function_sighashes array<STRING>,
  is_erc20 BOOLEAN,
  is_erc721 BOOLEAN,
  block_number BIGINT,
  block_hash STRING,
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
LOCATION 's3://<your_bucket>/export/contracts/';

MSCK REPAIR TABLE contracts;