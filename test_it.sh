#!/bin/bash
python -m battle_city.server&
P1=$!
sleep 2
python -m battle_city.client > /dev/null&
P2=$!
python -m battle_city.client > /dev/null&
P3=$!

echo pids: $P1 $P2 $P3

echo "enter to cancel..."
read foobar
kill -9 $P1 $P2 $P3 

