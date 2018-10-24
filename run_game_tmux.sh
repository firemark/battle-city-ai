#!/bin/bash
set -e

CMD_A='python -m battle_city.examples.python.radom'
CMD_B='python -m battle_city.examples.python.radom'
CMD_C='python -m battle_city.examples.python.radom'
CMD_D='python -m battle_city.examples.python.radom'
source _run_game.sh

SESSION=${USER}_BATTLECITY

tmux -2 new-session -d -s $SESSION "/bin/sh"

# top window - server
tmux select-pane -t 0
tmux send-keys "trap finish INT" C-m
tmux send-keys "trap finish exit" C-m
tmux send-keys "finish() { tmux kill-session -t $SESSION; }" C-m
tmux send-keys "clear; echo 'press CTRL+C (^C) or CTRL+D (^D) to close.'" C-m
tmux send-keys "${SERVER_CMD}" C-m
tmux send-keys "echo 'press CTRL+C (^C) or CTRL+D (^D) to close.'" C-m

tmux split-window -v -p 80 "/bin/sh"
tmux split-window -h "/bin/sh"

if [ $MAX_PLAYERS -ge 3 ]; then
    tmux select-pane -t 1
    tmux split-window -v "/bin/sh"
fi

if [ $MAX_PLAYERS -ge 4 ]; then
    tmux select-pane -t 3
    tmux split-window -v "/bin/sh"
fi

i=1
while [ $i -le $MAX_PLAYERS ]; do
    sleep 0.25
    tmux select-pane -t $i
    tmux send-keys "echo PLAYER $i; sleep 2 && ${CMDS[$i]}" C-m
    ((i++))
done

# return to server window
tmux select-pane -t 0

tmux -2 attach-session -t $SESSION
