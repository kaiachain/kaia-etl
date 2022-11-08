# Quickstart
Install Klaytn ETL:

```bash
pip3 install klaytn-etl-cli
```

Export blocks and transactions

```bash
> klaytnetl export_blocks_and_transactions --start-block 0 --end-block 5000 \
--blocks-output blocks.json --transactions-output transactions.json
```

Export ERC20 and ERC721 transfers

```bash
> klaytnetl export_token_transfers --start-block 0 --end-block 5000 \
--output token_transfers.json
```

Export traces

```bash
> klaytnetl export_traces --start-block 0 --end-block 5000 \
--output traces.json
```

Find other commands [here](klaytnetl/cli/__init__.py).

For the latest version, check out the repo and call 
```bash
> pip3 install -e . 
> python3 klaytnetl.py
```
