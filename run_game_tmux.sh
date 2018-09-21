#!/bin/bash
set -e
source _run_game.sh

SESSION=${USER}_BATTLECITY

tmux -2 new-session -d -s $SESSION "/bin/sh"

# top window - server
tmux split-window -v "/bin/sh"
tmux select-pane -t 0
tmux send-keys "clear; python -m battle_city.server --ip $IP --port $PORT --map $MAP --speed $SPEED $SERVER_OPTS; read; tmux kill-session -t $SESSION" C-m

# player windows
tmux select-pane -t 1 
tmux split-window -h "/bin/sh"

# left window - 1st player
tmux select-pane -t 1
tmux send-keys "clear; echo PLAYER 1; sleep 2 && $CMD_A" C-m

# right window - 2nd player
tmux select-pane -t 2
tmux send-keys "clear; echo PLAYER 2; sleep 2 && $CMD_B" C-m

# return to server window
tmux select-pane -t 0

tmux -2 attach-session -t $SESSION
