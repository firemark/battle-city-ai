#!/bin/bash
set -e

CMD_A="python -m battle_city.client"
CMD_B="python -m battle_city.client"
while getopts a:b:h option; do
    case $option in
        a) CMD_A=$OPTARG;;
        b) CMD_B=$OPTARG;;
        h) echo "cat this file"; exit;;
    esac
done

SESSION=$USER-BATTLECITY

tmux -2 new-session -d -s $SESSION "/bin/sh"

# top window - server
tmux split-window -v "/bin/sh"
tmux select-pane -t 0
tmux send-keys "python -m battle_city.server; read; tmux kill-server" C-m

# player windows
tmux select-pane -t 1 
tmux split-window -h "/bin/sh"

# left window - 1st player
tmux select-pane -t 1
tmux send-keys "echo PLAYER 1; sleep 2 && $CMD_A" C-m

# right window - 2nd player
tmux select-pane -t 2
tmux send-keys "echo PLAYER 2; sleep 2 && $CMD_B" C-m

# return to server window
tmux select-pane -t 0

tmux -2 attach-session -t $SESSION
