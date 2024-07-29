#!/bin/bash

CYPRESS_RPC_URL=${CYPRESS_RPC_URL:-}

if [ -z "$CYPRESS_RPC_URL" ]; then
    echo "Environment variable CYPRESS_RPC_URL is not set"
    exit 1
fi

python klaytnetl.py export_trace_group_kafka \
    --start-block 154474144 \
    --end-block 154474164 \
    --provider-uri $CYPRESS_RPC_URL \
    --kafka-uri localhost:9092 \
    --kafka-topic local.klaytn.chaindatafetcher.en-0.tracegroup.v1 \
    --kafka-group-id test-consumer1 \
    -b 100 \
    -t 180 \
    --compress \
    --file-format json \
    --file-maxlines 10000 \
    --log-percentage-step 1 \
    --traces-output test_output
