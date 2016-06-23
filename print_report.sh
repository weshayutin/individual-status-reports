#!/bin/bash
source environment.sh

RPM_REQS='python-feedparser python-bugzilla pytz python-dateutil python-devel'
COMMAND='python2 reports/individual_report.py #| tee > ~/Documents/ENGINEERING_REPORTS/report_`date +%Y-%m-%d`.txt'

echo "Checking dependencies"
rpm -q $RPM_REQS &> /tmp/req_check.log
REQUIREMENTS=$?

if [ -z "$TEAM" ] || [ -z $trello_token ] || [ -z $BZ_USER ]; then
    echo "please fill out the TEAM, trello, and bugzilla env variables in environment.sh"
    exit 1
fi

if [[ $REQUIREMENTS == 0 ]]; then
    echo "Requirements are already installed"
    $COMMAND
else
    echo "Missing requirements, Installing $RPM_REQS"
    sleep 5;
    sudo yum install -y  $RPM_REQS
    $COMMAND
fi
