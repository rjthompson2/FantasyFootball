#!/bin/sh

#TODO need to run each one parallely in different terminals
open -a Terminal "`commands/run_data_visualization.sh`"
open -a Terminal "`commands/run_drafter_gui.sh`"
python frontend/webapp/app.py