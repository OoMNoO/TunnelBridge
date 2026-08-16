#!/bin/bash

#tmux kill-session -t reverse-ssh 2>/dev/null

pkill -f "autossh.*-R 2223:localhost:22"

tmux kill-session -t reverse-ssh 2>/dev/null