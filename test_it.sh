#!/bin/bash
trap finish INT

function finish() {
    kill -9 $P1 $P2 $P3
}

echo "^C to cancel..."

python -m battle_city.server&
P1=$!
sleep 2
python -m battle_city.client > /dev/null&
P2=$!
python -m battle_city.client > /dev/null&
P3=$!

echo pids: $P1 $P2 $P3

wait $P1
wait $P2
wait $P3
