#!/bin/bash
set -e
trap finish INT

finish() {
    kill -9 $P1 $P2 $P3
}

CMD_A='python -m battle_city.client'
CMD_B='python -m battle_city.client silent'
source _run_game.sh
echo "^C to cancel..."

python -m battle_city.server --ip $IP --port $PORT --map $MAP --speed $SPEED $SERVER_OPTS&
P1=$!
sleep 2
$CMD_A | sed -s 's/^/CLIENT 1: /'&
P2=$!
sleep 0.25
$CMD_B | sed -s 's/^/CLIENT 2: /'&
P3=$!

echo pids: $P1 $P2 $P3

wait $P1
wait $P2
wait $P3

