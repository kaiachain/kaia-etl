#!/bin/bash

# Modify testdata_154474164.json to contain a very long dummy string
echo "Modifying testdata_154474164.json..."
jq -c '.[0].result.value = "0x" + "aa" * 100000000' testdata_154474164.json > testdata_9999999999.json

echo "Modification complete."

