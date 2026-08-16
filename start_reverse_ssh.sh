#!/bin/bash

SESSION="reverse-ssh"

tmux has-session -t "$SESSION" 2>/dev/null
if [ $? -ne 0 ]; then
    tmux new-session -d -s "$SESSION" \
    "autossh -M 0 -N \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes \
    -R 2223:localhost:22 \
    USER@HOST -p PORT -i /path/to/ssh/key"
fi