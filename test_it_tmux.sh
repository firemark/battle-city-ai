#!/bin/bash
set -e

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
tmux send-keys "echo PLAYER 1; sleep 2 && python -m battle_city.client" C-m

# right window - 2nd player
tmux select-pane -t 2
tmux send-keys "echo PLAYER 2; sleep 2 && python -m battle_city.client" C-m

# return to server window
tmux select-pane -t 0

tmux -2 attach-session -t $SESSION
