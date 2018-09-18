#!/bin/bash
set -e
trap finish INT

function finish() {
    kill -9 $P1 $P2 $P3
}

CMD_A="python -m battle_city.client"
CMD_B="python -m battle_city.client"
while getopts a:b:h option; do
    case $option in
        a) CMD_A=$OPTARG;;
        b) CMD_B=$OPTARG;;
        h) echo "cat this file"; exit;;
    esac
done

echo "^C to cancel..."

python -m battle_city.server&
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
