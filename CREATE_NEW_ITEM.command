#!/bin/bash
cd "$(dirname "$0")"

source ./code/venv/bin/activate
clear
python ./code/main.py
# exit
osascript -e 'tell application "Terminal" to close front window' & exit