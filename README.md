# Klaytn ETL

Klaytn ETL lets you convert Klaytn blockchain data into convenient formats like JSONs, CSVs and relational databases.
This is a fork of [Ethereum ETL](https://github.com/blockchain-etl/ethereum-etl).

[Full documentation available here](http://klaytn-etl.readthedocs.io/).

***Notice: Klaytn ETL is still on the beta version. However, CLIs are all functional.***

## Quickstart
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

### Running in Docker

1. Install Docker https://docs.docker.com/install/

2. Build a docker image
    ```bash
    > docker build -t klaytn-etl:latest .
    > docker image ls
    ```

3. Run a container out of the image
    ```bash
    > docker run -v $HOME/output:/klaytn-etl/output klaytn-etl:latest export_all -s 0 -e 5499999 -b 100000
    > docker run -v $HOME/output:/klaytn-etl/output klaytn-etl:latest export_all -s 2018-01-01 -e 2018-01-01
    ```
