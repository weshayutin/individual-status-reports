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

# setup logging directory
mkdir -p ~/Documents/ENGINEERING_REPORTS/

exec &> >(tee -ia ~/Documents/ENGINEERING_REPORTS/"$TEAM"_report_`date +%Y-%m-%d`.txt )

if [ -f team_$TEAM.sh ]; then
    source team_$TEAM.sh
else
    echo "missing file team_$TEAM.sh"
    exit
fi

if [ -f environment.sh ]; then
    source environment.sh
else
    echo "missing file environment.sh"
    exit
fi

bash check_env.sh

COMMAND='python2 reports/individual_report.py'
echo $COMMAND
$COMMAND

echo ""
echo "TRIPLEO-QUICKSTART review stats"
gerrymander patchreviewstats --project openstack/tripleo-quickstart
echo ""
echo "TRIPLEO-QUICKSTART-EXTRAS review stats"
gerrymander patchreviewstats --project openstack/tripleo-quickstart-extras
