TRANSACTIONS_SCHEMA = [
    {
        "name": "hash",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Hash of the transaction",
    },
    {
        "name": "nonce",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "The number of transactions made by the sender prior to this one",
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
        "name": "transaction_index",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Integer of the transactions index position in the block",
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
        "description": "Address of the receiver. null when its a contract creation transaction",
    },
    {
        "name": "value",
        "type": "DECIMAL",
        "mode": "NULLABLE",
        "description": "Value transferred in Peb",
    },
    {
        "name": "gas",
        "type": "DECIMAL",
        "mode": "NULLABLE",
        "description": "Gas provided by the sender",
    },
    {
        "name": "gas_price",
        "type": "DECIMAL",
        "mode": "NULLABLE",
        "description": "Gas price provided by the sender in Peb",
    },
    {
        "name": "input",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "The data sent along with the transaction",
    },
    {
        "name": "fee_payer",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "(optional) Address of the fee payer",
    },
    {
        "name": "fee_payer_signatures",
        "type": "STRUCT",
        "mode": "REPEATED",
        "fields": [
            {"name": "V", "type": "STRING"},
            {"name": "R", "type": "STRING"},
            {"name": "S", "type": "STRING"},
        ],
        "description": "(optional) An array of fee payer’s signature objects. A signature object contains three fields (V, R, and S). V contains ECDSA recovery id. R contains ECDSA signature r while S contains ECDSA signature s",
    },
    {
        "name": "fee_ratio",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "(optional) Fee ratio of the fee payer. If it is 30, 30% of the fee will be paid by the fee payer. 70% will be paid by the sender",
    },
    {
        "name": "sender_tx_hash",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Hash of a transaction that is signed only by the sender",
    },
    {
        "name": "signatures",
        "type": "STRUCT",
        "mode": "REPEATED",
        "fields": [
            {"name": "V", "type": "STRING"},
            {"name": "R", "type": "STRING"},
            {"name": "S", "type": "STRING"},
        ],
        "description": "An array of signature objects. A signature object contains three fields (V, R, and S). V contains ECDSA recovery id. R contains ECDSA signature r while S contains ECDSA signature s",
    },
    {
        "name": "tx_type",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "A string representing the type of the transaction",
    },
    {
        "name": "tx_type_int",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "An integer representing the type of the transaction",
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
        "name": "receipt_gas_used",
        "type": "DECIMAL",
        "mode": "NULLABLE",
        "description": "The amount of gas used by this specific transaction alone",
    },
    {
        "name": "receipt_contract_address",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "The contract address created, if the transaction was a contract creation, otherwise null",
    },
    {
        "name": "receipt_status",
        "type": "INT64",
        "mode": "NULLABLE",
        "description": "Either 1 (success) or 0 (failure) (post Byzantium)",
    },
    {
        "name": "max_priority_fee_per_gas",
        "type": "DECIMAL",
        "mode": "NULLABLE",
        "description": "A maximum amount to pay for the transaction to execute",
    },
    {
        "name": "max_fee_per_gas",
        "type": "DECIMAL",
        "mode": "NULLABLE",
        "description": "Gas tip cap for dynamic fee transaction in peb",
    },
    {
        "name": "access_list",
        "type": "STRUCT",
        "mode": "REPEATED",
        "fields": [
            {"name": "address", "type": "STRING"},
            {"name": "storage_keys", "type": "STRING", "mode": "REPEATED"},
        ],
        "description": "An array of accessList",
    },
]
