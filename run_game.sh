#!/bin/bash
set -e
trap finish INT

finish() {
    kill -9 $P1 $P2 $P3
}

CMD_A='python -m battle_city.examples.random'
CMD_B='python -m battle_city.examples.random silent'
source _run_game.sh
echo "^C to cancel..."

python -m battle_city.server --ip $IP --port $PORT --map $MAP --speed $SPEED $SERVER_OPTS&
P1=$!
sleep 2
eval "$CMD_A" | sed 's/^/CLIENT 1: /'&
P2=$!
sleep 0.25
eval "$CMD_B" | sed 's/^/CLIENT 2: /'&
P3=$!

echo pids: $P1 $P2 $P3

wait $P1
wait $P2
wait $P3

