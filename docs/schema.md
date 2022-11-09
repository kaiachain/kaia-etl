# Schema

## blocks.csv

Column              | Type       |
--------------------|------------|
number              | bigint     |
hash                | hex_string |
parent_hash         | hex_string |
logs_bloom          | hex_string |
transactions_root   | hex_string |
state_root          | hex_string |
receipts_root       | hex_string |
size                | bigint     |
extra_data          | hex_string |
gas_used            | numeric    |
block_timestamp     | timestamp  |
block_unix_timestamp| numeric    |
transaction_count   | bigint     |
block_score         | numeric    |
total_block_score   | numeric    |
governance_data     | hex_string |
vote_data           | hex_string |
committee           | struct     |
proposer            | hex_string |
reward_address      | adresss    |
base_fee_per_gas    | numeric    |

---

## transactions.csv

Column                  | Type         |
------------------------|--------------|
hash                    | hex_string   |
nonce                   | bigint       |
block_hash              | hex_string   |
block_number            | bigint       |
transaction_index       | bigint       |
from_address            | address      |
to_address              | address      |
value                   | numeric      |
gas                     | bigint       |
gas_price               | bigint       |
input                   | hex_string   |
fee_payer               | hex_string   |
fee_payer_signatures    | struct       |
fee_ratio               | bigint       |
sender_tx_hash          | hex_string   |
signatures              | struct       |
tx_type                 | string       |
tx_type_int             | bigint       |
block_timestamp         | timestamp    |
block_unix_timestamp    | numeric      |
receipt_gas_used        | numeric      |
receipt_contract_address| adresss      |
receipt_status          | bigint       |
max_priority_fee_per_gas| numeric      |
max_fee_per_gas         | numeric      |
access_list             | struct       |

---

## token_transfers.csv

Column                      | Type       |
----------------------------|------------|
token_address               | address    |
from_address                | address    |
to_address                  | address    |
value                       | string     |
block_hash                  | hex_string |
block_number                | bigint     |
block_timestamp             | timestamp  |
block_unix_timestamp        | numeric    |
transaction_hash            | hex_string |
transaction_receipt_status  | bigint     |
log_index                   | bigint     |

---

## receipts.csv

Column                       | Type       |
-----------------------------|------------|
transaction_hash             | hex_string |
transaction_index            | bigint     |
block_hash                   | hex_string |
block_number                 | bigint     |
gas                          | numeric    |
gas_price                    | numeric    |
gas_used                     | numeric    |
effective_gas_price          | numeric    |
contract_address             | address    |
logs_bloom                   | hex_string |
nonce                        | bigint     |
fee_payer                    | hex_string |
fee_payer_signatures         | struct     |
fee_ratio                    | bigint     |
code_format                  | string     |
human_readable               | boolean    |
tx_error                     | string     |
key                          | hex_string |
input_data                   | hex_string |
from_address                 | address    |
to_address                   | address    |
type_name                    | string     |
type_int                     | bigint     |
sender_tx_hash               | hex_string |
signatures                   | struct     |
status                       | bigint     |
value                        | string     |
input_json                   | struct     |
access_list                  | struct     |
chain_id                     | bigint     |
max_priority_fee_per_gas     | numeric    |
max_fee_per_gas              | numeric    |
block_timestamp              | timestamp  |
block_unix_timestamp         | numeric    |

---

## logs.csv

Column                       | Type       |
-----------------------------|------------|
block_number                 | bigint     |
block_hash                   | hex_string |
block_timestamp              | timestamp  |
block_unix_timestamp         | numeric    |
transaction_hash             | hex_string |
transaction_index            | bigint     |
transaction_receipt_status   | bigint     |
log_index                    | bigint     |
address                      | address    |
data                         | string     |
topics                       | string     |

---

## contracts.csv

Column                       | Type       |
-----------------------------|------------|
address                      | address    |
bytecode                     | hex_string |
function_sighashes           | string     |
is_erc20                     | boolean    |
is_erc721                    | boolean    |
is_erc1155                   | boolean    |
block_number                 | bigint     |
block_hash                   | hex_string |
block_timestamp              | timestamp  |
block_unix_timestamp         | numeric    |
transaction_hash             | hex_string |
transaction_index            | bigint     |
transaction_receipt_status   | bigint     |
trace_index                  | bigint     |
trace_status                 | bigint     |
creator_address              | address    |

---

## tokens.csv

Column                       | Type       |
-----------------------------|------------|
address                      | address    |
symbol                       | string     |
name                         | string     |
decimals                     | bigint     |
total_supply                 | string     |
function_sighashes           | string     |
is_erc20                     | boolean    |
is_erc721                    | boolean    |
is_erc1155                   | boolean    |
block_number                 | bigint     |
block_hash                   | hex_string |
block_timestamp              | timestamp  |
block_unix_timestamp         | numeric    |
transaction_hash             | hex_string |
transaction_index            | bigint     |
transaction_receipt_status   | bigint     |
trace_index                  | bigint     |
trace_status                 | bigint     |
creator_address              | address    |

---

## traces.csv

Column                       | Type       |
-----------------------------|------------|
block_number                 | bigint     |
block_hash                   | hex_string |
block_timestamp              | timestamp  |
block_unix_timestamp         | numeric    |
transaction_hash             | hex_string |
transaction_index            | bigint     |
transaction_receipt_status   | bigint     |
from_address                 | address    |
to_address                   | address    |
value                        | numeric    |
input                        | hex_string |
output                       | hex_string |
trace_type                   | string     |
call_type                    | string     |
gas                          | numeric    |
gas_used                     | numeric    |
subtraces                    | bigint     |
trace_address                | string     |
error                        | string     |
status                       | bigint     |
trace_index                  | string     |

You can find column descriptions in [https://github.com/klaytn/klaytn-etl](https://github.com/klaytn/klaytn-etl/tree/main/schemas)

Note: for the `address` type all hex characters are lower-cased.
`boolean` type can have 2 values: `True` or `False`.
