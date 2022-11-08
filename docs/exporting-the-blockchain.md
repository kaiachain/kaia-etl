## Exporting the Blockchain

1. Install python 3.7.2+: [https://www.python.org/downloads/](https://www.python.org/downloads/)

1. Launch an endpoint node (https://docs.klaytn.foundation/getting-started/quick-start/launch-an-en) or use pre-existing endpoint (https://docs.klaytn.foundation/dapp/json-rpc/public-en)
 
1. Install Klaytn ETL: `> pip3 install klaytn-etl-cli`

1. Export all:

```bash
> klaytnetl export_all --help
> klaytnetl export_all -s 0 -e 5999999 -b 100000  -p https://cypress.fandom.finance/archive -o output
```
    
In case `klaytnetl` command is not available in PATH, use `python3 -m klaytnetl` instead.

The result will be in the `output` subdirectory, partitioned in Hive style:
```bash
output/blocks/start_block=00000000/end_block=00099999/blocks_00000000_00099999.csv
output/blocks/start_block=00100000/end_block=00199999/blocks_00100000_00199999.csv
...
output/transactions/start_block=00000000/end_block=00099999/transactions_00000000_00099999.csv
...
output/token_transfers/start_block=00000000/end_block=00099999/token_transfers_00000000_00099999.csv
...
```

Should work on Linux, Mac, Windows.
Since `debug_traceBlockByNumber` takes a long time, please cautious when running anything related to trace.
