#!/bin/bash
set -e
trap finish INT

function finish() {
    kill -9 $P1 $P2 $P3
}

source _run_game.sh
echo "^C to cancel..."

python -m battle_city.server --ip $IP --port $PORT --map $MAP $SERVER_OPTS&
P1=$!
sleep 2
$CMD_A > /dev/null&
P2=$!
$CMD_B > /dev/null&
P3=$!

echo pids: $P1 $P2 $P3

wait $P1
wait $P2
wait $P3
