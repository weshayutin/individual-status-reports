#!/usr/bin/python

import ast
import os
from datetime import datetime

import ReportToolbox as report
import TrelloToolbox as trello
import pytz

# Global variables
now = datetime.now(pytz.utc)
team = ast.literal_eval(os.environ['TEAM'])
recent = ast.literal_eval(os.environ['RECENT'])

_myToken = os.environ.get('trello_token')

apiContextTrello = trello.ApiContext(_myToken)
membersHelper = trello.Members(apiContextTrello)
reportHelper = report.Report()

if __name__ == "__main__":
    for member in team:
        m = membersHelper.get_member_id(team[member]['trello'])
        # print out active trello cards
        print('\t {} {} {} {}\n'.format("=" * 60, member.upper(), "ENGINEERING REPORT", "=" * 60))
        reportHelper.print_active_cards(m, recent)
        print("\n")
        # print out gerrit reviews
        reportHelper.print_reviews(team[member]['openstack'], team[member]['gerrithub'], team[member]['rh_email'], recent)
        print("\n\n\n")
        # print out launchpad bugs
        reportHelper.print_launch_pad_bugs(team[member]['openstack'], recent)
        print("\n\n\n")
        reportHelper.print_bugzilla_bugs(member, recent)
        print("\n\n\n")
