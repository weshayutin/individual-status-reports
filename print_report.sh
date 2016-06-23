#!/bin/bash
source environment.sh
bash check_env.sh

COMMAND='python2 reports/individual_report.py #| tee > ~/Documents/ENGINEERING_REPORTS/report_`date +%Y-%m-%d`.txt'

$COMMAND
