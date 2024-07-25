#!/bin/bash

CYPRESS_RPC_URL=${CYPRESS_RPC_URL:-}

if [ -z "$CYPRESS_RPC_URL" ]; then
    echo "Environment variable CYPRESS_RPC_URL is not set"
    exit 1
fi

for block in $(seq 154474144 154474164); do
    echo "Tracing block $block..."
    cast rpc debug_traceBlockByNumber $block '{"tracer":"fastCallTracer"}' -r $CYPRESS_RPC_URL > testdata_$block.json
done
