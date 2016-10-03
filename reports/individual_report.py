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

    summary_cards = {}
    summary_gerrit = {}
    summary_lp_bugs = {}
    summary_bz_bugs = {}

    for member in team:
        m = membersHelper.get_member_id(team[member]['trello'])
        # print out active trello cards
        print('\t {} {} {} {}\n'.format("=" * 60, member.upper(), "ENGINEERING REPORT", "=" * 60))
        person_trello, cards = reportHelper.print_active_cards(m, recent)
        summary_cards[person_trello] = cards
        print("\n")

        # print out gerrit reviews
        person_gerrit, reviews = reportHelper.print_reviews(team[member]['openstack'], team[member]['gerrithub'], team[member]['rh_email'], team[member]['rdoproject'], recent)
        summary_gerrit[person_gerrit] = reviews
        print("\n\n\n")

        # print out launchpad bugs
        person_launchpad, lp_bugs = reportHelper.print_launch_pad_bugs(team[member]['openstack'], recent)
        summary_lp_bugs[person_launchpad] = lp_bugs
        print("\n\n\n")

        # print out bz bugs
        person_bugzilla, bz_bugs = reportHelper.print_bugzilla_bugs(member, recent)
        summary_bz_bugs[person_bugzilla] = bz_bugs
        print("\n\n\n")

    print("Summary:")
    print("=" * 100 + "\n\n")
    print("Trello Summary:\n")
    print(summary_cards)
    print("\n\n")
    print("Gerrit Summary:\n")
    print(summary_gerrit)
    print("\n\n")
    print("LaunchPad Bug Summary:\n")
    print(summary_lp_bugs)
    print("\n\n")
    print("Bugzilla Bug Summary:\n")
    print(summary_bz_bugs)
    print("\n\n")


