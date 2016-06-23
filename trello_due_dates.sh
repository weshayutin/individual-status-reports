#!/bin/bash
source environment.sh
bash check_env.sh


COMMAND='python2 reports/OverDueTrello.py #| tee > ~/Documents/ENGINEERING_REPORTS/report_`date +%Y-%m-%d`.txt'

$COMMAND
