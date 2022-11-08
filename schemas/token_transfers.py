TOKEN_TRANSFERS_SCHEMA = [
    {
        "name": "token_address",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Token address",
    },
    {
        "name": "from_address",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Address of the sender",
    },
    {
        "name": "to_address",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Address of the receiver",
    },
    {
        "name": "value",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Amount of tokens transferred (ERC20) / id of the token transferred (ERC721). Use safe_cast for casting to NUMERIC or FLOAT64",
    },
    {
        "name": "block_hash",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Hash of the block",
    },
    {
        "name": "block_number",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Block number corresponding",
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
        "description": "Hash of the transactions",
    },
    {
        "name": "transaction_index",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Integer of the transactions index position in the block",
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
]
