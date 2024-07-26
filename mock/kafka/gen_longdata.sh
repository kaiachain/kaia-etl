#!/bin/bash

# Modify testdata_154474164.json to contain a very long dummy string
echo "Modifying testdata_154474164.json..."
jq -c '.result.[0].result.value = "0x" + "aa" * 100000000' testdata_154474164.json > testdata_12345.json

echo "Modification complete."

