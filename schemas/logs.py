LOGS_SCHEMA = [
    {
        "name": "block_number",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Block number corresponding",
    },
    {
        "name": "block_hash",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Hash of the block",
    },
    {
        "name": "block_timestamp",
        "type": "TIMESTAMP",
        "mode": "NULLABLE",
        "description": "The UTC timestamp for when the block was collated",
    },
    {
        "name": "block_unix_timestamp",
        "type": "FLOAT64",
        "mode": "NULLABLE",
        "description": "The unix timestamp for when the block was collated",
    },
    {
        "name": "transaction_hash",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Integer of the transactions index position in the block",
    },
    {
        "name": "transaction_index",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Hash of the transactions",
    },
    {
        "name": "transaction_receipt_status",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Either 1 (success) or 0 (failure) (post Byzantium)",
    },
    {
        "name": "log_index",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Integer of the log index position in the block",
    },
    {
        "name": "address",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Address from which this log originated",
    },
    {
        "name": "data",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Contains one or more 32 Bytes non-indexed arguments of the log",
    },
    {
        "name": "topics",
        "type": "STRING",
        "mode": "REPEATED",
        "description": "Indexed log arguments (0 to 4 32-byte hex strings). (In solidity: The first topic is the hash of the signature of the event (e.g. Deposit(address,bytes32,uint256)), except you declared the event with the anonymous specifier.)",
    },
]
