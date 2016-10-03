#!/bin/bash

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -t|--team)
    TEAM="$2"
    shift
    ;;
    -h|--help)
    HELP="$2"
    shift
    ;;
    *)
    ;;
esac
shift
done

function usage
{
    echo "usage: print_report.sh  [ -t team_name [direct_reports, rdo_infra] ] [-h --help]"
}

if [[ -z $TEAM ]]; then
    usage
    exit -1
fi

if [[ $HELP ]]; then
   usage
fi



echo SELECTED TEAM = "${TEAM}"


source team_$TEAM.sh
source environment.sh
bash check_env.sh

COMMAND='python2 reports/individual_report.py #| tee > ~/Documents/ENGINEERING_REPORTS/report_`date +%Y-%m-%d`.txt'

$COMMAND
