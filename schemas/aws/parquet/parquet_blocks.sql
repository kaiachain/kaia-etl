CREATE EXTERNAL TABLE IF NOT EXISTS parquet_blocks (
  number BIGINT,
  hash STRING,
  parent_hash STRING,
  logs_bloom STRING,
  transactions_root STRING,
  state_root STRING,
  receipts_root STRING,
  block_score DECIMAL(38,0) ,
  total_block_score DECIMAL(38,0),
  size BIGINT,
  extra_data STRING,
  gas_used BIGINT ,
  timestamp TIMESTAMP,
  unix_timestamp DOUBLE,
  transaction_count BIGINT,
  governance_data STRING,
  vote_data STRING,
  proposer STRING,
  committee array<STRING>.
  reward_address STRING,
  base_fee_per_gas DECIMAL(38, 0)
)
PARTITIONED BY (start_block BIGINT, end_block BIGINT)
STORED AS PARQUET
LOCATION 's3://<your_bucket>/klaytnetl/parquet/blocks';

MSCK REPAIR TABLE parquet_blocks;