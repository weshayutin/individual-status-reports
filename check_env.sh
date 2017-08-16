#!/bin/bash
source environment.sh

RPM_REQS='python-feedparser python-bugzilla pytz python-dateutil python-devel python2-numpy gerrymander'

echo "Checking dependencies"
rpm -q $RPM_REQS &> /tmp/req_check.log
REQUIREMENTS=$?

if [ -z "$TEAM" ] || [ -z $trello_token ] || [ -z $BZ_USER ]; then
    echo "please fill out the TEAM, trello, and bugzilla env variables in environment.sh"
    exit 1
fi

if [[ $REQUIREMENTS == 0 ]]; then
    echo "Requirements are already installed"
else
    echo "Missing requirements, Installing $RPM_REQS"
    sleep 5;
    sudo dnf install -y  $RPM_REQS
fi

