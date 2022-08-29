CREATE EXTERNAL TABLE IF NOT EXISTS transactions (
  hash STRING,
  nonce BIGINT,
  block_hash STRING,
  block_number BIGINT,
  transaction_index BIGINT,
  from_address STRING,
  to_address STRING,
  value DECIMAL(38, 0),
  gas DECIMAL(38, 0),
  gas_price DECIMAL(38, 0),
  input STRING,
  fee_payer STRING,
  fee_payer_signatures ARRAY<STRUCT<V:STRING, R:STRING, S:STRING>>,
  fee_ratio BIGINT,
  sender_tx_hash STRING,
  signatures ARRAY<STRUCT<V:STRING, R:STRING, S:STRING>>,
  tx_type STRING,
  tx_type_int BIGINT,
  max_priority_fee_per_gas DECIMAL(38, 0),
  max_fee_per_gas DECIMAL(38,0),
  block_timestamp TIMESTAMP,
  block_unix_timestamp DOUBLE,
  receipt_gas_used BIGINT,
  receipt_contract_address STRING,
  receipt_status BIGINT
)
PARTITIONED BY (block_date STRING)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://<your_bucket>/export/transactions/';

MSCK REPAIR TABLE transactions;