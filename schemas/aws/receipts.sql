CREATE EXTERNAL TABLE IF NOT EXISTS receipts (
  transaction_hash STRING,
  transaction_index BIGINT,
  block_hash STRING,
  block_number BIGINT,
  gas DECIMAL(38, 0),
  gas_price DECIMAL(38, 0),
  gas_used DECIMAL(38, 0),
  effective_gas_price DECIMAL(38, 0),
  contract_address STRING,
  logs_bloom STRING,
  nonce BIGINT,
  fee_payer STRING,
  fee_payer_signatures ARRAY<STRUCT<V:STRING, R:STRING, S:STRING>>,
  fee_ratio BIGINT,
  code_format STRING,
  human_readable BOOLEAN,
  tx_error STRING,
  key STRING,
  input_data STRING,
  from_address STRING,
  to_address STRING,
  type_name STRING,
  type_int BIGINT,
  sender_tx_hash STRING,
  signatures ARRAY<STRUCT<V:STRING, R:STRING, S:STRING>>,
  value DECIMAL(38, 0),
  chain_id BIGINT,
  max_priority_fee_per_gas DECIMAL(38, 0),
  max_fee_per_gas DECIMAL(38,0)
)
PARTITIONED BY (block_date STRING)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://<your_bucket>/export/receipts/';

MSCK REPAIR TABLE receipts;