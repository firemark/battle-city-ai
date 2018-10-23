#!/bin/bash
set -e
trap finish INT

PROGS=()
finish() {
    kill -9 ${PROGS[*]}
}

CMD_A='python -m battle_city.examples.python.random'
CMD_B='python -m battle_city.examples.python.random silent'
CMD_C='python -m battle_city.examples.python.random silent'
CMD_D='python -m battle_city.examples.python.random silent'
source _run_game.sh

echo "^C to cancel..."
$SERVER_CMD&
PROGS+=($!)
sleep 1.75

i=1
while [ $i -le $MAX_PLAYERS ]; do
    sleep 0.25
    ${CMDS[$i]} | sed "s/^/CLIENT $i: /"&
    PROGS+=($!)
    ((i++))
done

echo pids: $PROGS

for pid in ${PROGS[*]}; do
    wait $pid
done
