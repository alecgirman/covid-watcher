jq < *.covid.county.json '.message[].confirmed' | awk '{s+=$1} END {print s}'
