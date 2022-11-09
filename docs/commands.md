# Commands

All the commands accept `-h` parameter for help, e.g.:

```bash
> klaytnetl export_blocks_and_transactions -h

Usage: klaytnetl export_blocks_and_transactions [OPTIONS]

Options:
  -s, --start-block INTEGER   Start block  [default: 0]
  -e, --end-block INTEGER     End block  [required]
  -b, --batch-size INTEGER    The number of blocks to export at a time.
                              [default: 100]
  -p, --provider-uri TEXT     The URI of the web3 provider e.g.
                              file://$HOME/var/kend/data/klay.ipc or
                              https://cypress.fandom.finance/archive
                              [default:
                              https://cypress.fandom.finance/archive]
  -w, --max-workers INTEGER   The maximum number of workers.  [default: 5]
  --blocks-output TEXT        The output file for blocks. If not provided
                              blocks will not be exported. Use "-" for stdout
  --transactions-output TEXT  The output file for transactions. If not
                              provided transactions will not be exported. Use
                              "-" for stdout
  --network TEXT              Input either baobab or cypress to obtain public
                              provider.If not provided, the option will be
                              disabled.
  -h, --help                  Show this message and exit.
```

For the `--output` parameters the supported types are csv and json. The format type is inferred from the output file name.

#### export_blocks_and_transactions

```bash
> klaytnetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--provider-uri https://cypress.fandom.finance/archive \
--blocks-output blocks.csv --transactions-output transactions.csv
```

- Omit `--blocks-output` or `--transactions-output` options if you want to export only transactions/blocks.

- You can tune `--batch-size`, `--max-workers` for performance.

- You can select either `baobab` or `cypress` in `--network`.

[Blocks and transactions schema](schema.md#blockscsv).

#### export_token_transfers

```bash
> klaytnetl export_token_transfers --start-block 0 --end-block 500000 \
--provider-uri https://cypress.fandom.finance/archive --batch-size 100 --output token_transfers.csv
```

Include `--tokens <token1> --tokens <token2>` to filter only certain tokens, e.g.

```bash
> klaytnetl export_token_transfers --start-block 42397700 --end-block 42397800 \
--provider-uri https://cypress.fandom.finance/archive --output token_transfers.csv \
--tokens 0xcee8faf64bb97a73bb51e115aa89c17ffa8dd167 --tokens 0x34d21b1e550d73cee41151c77f3c73359527a396
```

- You can tune `--batch-size`, `--max-workers` for performance.

- You can select either `baobab` or `cypress` in `--network`.

[Token transfers schema](schema.md#token_transferscsv).

#### export_receipts_and_logs

First extract transactions from [export_blocks_and_transactions](#export_blocks_and_transactions)

Then export receipts and logs from transactions.csv file:

```bash
> klaytnetl export_receipts_and_logs --transactions transactions.csv \
--provider-uri https://cypress.fandom.finance/archive --receipts-output receipts.csv --logs-output logs.csv
```

- Omit `--receipts-output` or `--logs-output` options if you want to export only logs/receipts.

- You can tune `--batch-size`, `--max-workers` for performance.

- You can select either `baobab` or `cypress` in `--network`.

[Receipts and logs schema](schema.md#receiptscsv).

#### extract_token_transfers

First export receipt logs with [export_receipts_and_logs](#export_receipts_and_logs).

Then extract transfers from the logs.csv file:

```bash
> klaytnetl extract_token_transfers --logs logs.csv --output token_transfers.csv
```

- You can tune `--batch-size`, `--max-workers` for performance.

- You can select either `baobab` or `cypress` in `--network`.

[Token transfers schema](schema.md#token_transferscsv).

#### export_contracts

First extract receipts from [export_receipts_and_logs](#export_receipts_and_logs)

Then export contracts:

```bash
> klaytnetl export_contracts --receipts receipts.csv \
--provider-uri https://cypress.fandom.finance/archive --output contracts.csv
```

- You can tune `--batch-size`, `--max-workers` for performance.

- You can select either `baobab` or `cypress` in `--network`.

[Contracts schema](schema.md#contractscsv).

#### export_tokens

First extract token addresses from `contracts.json`
(Exported with [export_contracts](#export_contracts)):

```bash
> klaytnetl filter_items -i contracts.json -p "item['is_erc20'] or item['is_erc721'] or item['is_erc1155']" | \
klaytnetl extract_field -f address -o token_addresses.txt
```

Then export ERC20 / ERC721 / ERC1155 tokens:

```bash
> klaytnetl export_tokens --token-addresses token_addresses.txt \
--provider-uri https://cypress.fandom.finance/archive --output tokens.csv
```

- You can tune `--max-workers` for performance.

- You can select either `baobab` or `cypress` in `--network`.

[Tokens schema](schema.md#tokenscsv).

#### export_traces

Also called internal transactions.
Since this is rerunning a block, this will take a long time based on the transactions that block contains.
Make sure your node is an archive node with at least 8GB of memory, or else you will face timeout errors. 
See [this issue](https://github.com/blockchain-etl/ethereum-etl/issues/137)

```bash
> klaytnetl export_traces --start-block 0 --end-block 500000 \
--provider-uri https://cypress.fandom.finance/archive --batch-size 100 --output traces.csv
```

- By adding `--enrich` flag, you can enrich output files with additional fields like `block-timestamp`.

- You can tune `--batch-size`, `--max-workers` for performance.

- You can set `--timeout` appropriately.

- You can set `--file-format` to either `csv` or `json` and manipulate by `--file-maxlines` and `--compress` 

- You can export to cloud storage by adding `--s3-bucket` flag.

- You can select either `baobab` or `cypress` in `--network`.

[Traces schema](schema.md#tracescsv).

#### export_block_group

Exports block groups - blocks, transactions, receipts, logs, token transfer - from Klaytn node.

```bash
> klaytnetl export_block_group --start-block 0 --end-block 500000 \
--provider-uri https://cypress.fandom.finance/archive --batch-size 100 \
--blocks-output blocks.csv --transactions-output transactions.csv \
--receipts-output receipts.csv --logs-output logs.csv --token-transfers-output token_transfer.csv
```

- Omit `--blocks-output`/`--transactions-output`/`--receipts-output`/`--logs-output`/`--token-transfers-output` options 
if you want to export only transactions/blocks/receipts/logs/token transfers.

- By adding `--enrich` flag, you can enrich output files with additional fields like `block-timestamp`.

- You can tune `--batch-size`, `--max-workers` for performance.

- You can set `--timeout` appropriately.

- You can set `--file-format` to either `csv` or `json` and manipulate by `--file-maxlines` and `--compress` 

- You can export to cloud storage by adding `--s3-bucket` or `--gcs-bucket` flag.

- You can select either `baobab` or `cypress` in `--network`.


#### export_trace_group

Exports trace groups - traces, contracts, tokens - from Klaytn node.
Since this is rerunning a block, this will take a long time based on the transactions that block contains.
Make sure your node is an archive node with at least 8GB of memory, or else you will face timeout errors. 

```bash
> klaytnetl export_trace_group --start-block 0 --end-block 500000 \
--provider-uri https://cypress.fandom.finance/archive --batch-size 100 \
--traces-output traces.csv --tokens-output tokens.csv --contracts-output contracts.csv
```

- Omit `--traces-output`/`--tokens-output`/`--contracts-output` options 
if you want to export only traces/tokens/contracts.

- By adding `--enrich` flag, you can enrich output files with additional fields like `block-timestamp`.

- You can tune `--batch-size`, `--max-workers` for performance.

- You can set `--timeout` appropriately.

- You can set `--file-format` to either `csv` or `json` and manipulate by `--file-maxlines` and `--compress` 

- You can export to cloud storage by adding `--s3-bucket` or `--gcs-bucket` flag.

- Use `--detailed-trace-log` and `--log-percentage-step` to get trace count with wanted steps. 

- You can select either `baobab` or `cypress` in `--network`.

#### get_block_range_for_date

```bash
> klaytnetl get_block_range_for_date --provider-uri=https://cypress.fandom.finance/archive --date 2020-01-01
16369455,16455852
```

#### get_keccak_hash

```bash
> klaytnetl get_keccak_hash -i "transfer(address,uint256)"
0xa9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b
```
