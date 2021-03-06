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
    HELP="true"
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

if [[ -v $HELP ]]; then
   usage
   exit
fi

if [[ -z $TEAM ]]; then
    usage
    exit -1
fi

echo SELECTED TEAM = "${TEAM}"

source team_$TEAM.sh
source environment.sh
bash check_env.sh

exec &> >(tee -ia ~/Documents/ENGINEERING_REPORTS/trello_`date +%Y-%m-%d`.txt )


COMMAND='python2 reports/OverDueTrello.py'

$COMMAND
