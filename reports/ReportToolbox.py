#!/usr/bin/python

import ast
import os
from datetime import datetime
from time import mktime

import BugzillaToolbox as bz
import GerritToolbox as gerrit
import LaunchPadToolbox as lpbugs
import TrelloToolbox as trello
import dateutil.parser
import pytz
from dateutil.relativedelta import *

import pdb

# Global variables
now = datetime.now(pytz.utc)
team = ast.literal_eval(os.environ['TEAM'])
_myToken = os.environ.get('trello_token')

# in a full SDK wrapper (not the goal here) this would live in __init__.py for a seperate module
apiContextTrello = trello.ApiContext(_myToken)
apiContextGerrit = gerrit.ApiContext()
apiContextLPBugs = lpbugs.ApiContext()
apiContextBugzilla = bz.ApiContext()

# note: the only state kept in these is the context object
boardsHelper = trello.Boards(apiContextTrello)
cardsHelper = trello.Cards(apiContextTrello)
membersHelper = trello.Members(apiContextTrello)
changesHelper = gerrit.Changes(apiContextGerrit)
lpbugsHelper = lpbugs.Bugs(apiContextLPBugs)
bzHelper = bz.Bugs(apiContextBugzilla)


class Report():
    def print_cards(self, cards, header=""):
        "Print a list of cards in a nice neat summary view"
        print(header)
        for c in cards:
            cn=c['name']
            bid=c['idBoard']
            surl=c['shortUrl']
            card_name=cn.encode('ascii', 'replace')
            board_id=bid.encode('ascii', 'replace')
            short_url=surl.encode('ascii', 'replace')

            print(
                '\t {0:>30s}: {1:>20s} {2:<.80}'.format(boardsHelper.get_name(board_id), short_url, card_name))

    def get_member_cards(self, member):
        # get the trello cards for the member from everyboard
        return membersHelper.get_member_cards(member)

    def print_active_cards(self, member, start_date):
        active_cards = []
        cards = self.get_member_cards(member)
        two_weeks_ago = now + relativedelta(weeks=start_date)
        since = two_weeks_ago.strftime("%Y-%m-%d")
        for c in cards:
            last_activity = dateutil.parser.parse(c['dateLastActivity'])
            if last_activity > two_weeks_ago:
                active_cards.append(c)

        header = '\t {} {} {} {} {}'.format("=============", membersHelper.get_member_name(member),
                                            "'s Active cards since " + since + " " + "================== Number of Cards: ",
                                            len(active_cards), "===========")
        self.print_cards(active_cards, header)
        return membersHelper.get_member_name(member), len(active_cards)

    def print_reviews(self, openstack_person, gerrithub_person, codeng_person, rdoproject_person, start_date):
        date = (now + relativedelta(weeks=start_date)).strftime("%Y-%m-%d")
        changes = changesHelper.get_open_changes_by_person(openstack_person, gerrithub_person, codeng_person, rdoproject_person, date)
        print('\t {0:>50s} {1:<70s} {2:>8s} {3:>10s} {4:.10s} {5:.10s}'.format("project", "subject", "id", "status",
                                                                               "created", "   updated"))
        print("=" * 5 + " Since " + date + " Total Open or Merged Gerrit Reviews: " + str(
            len(changes)) + "  " + "=" * 105)
        for c in changes:
            print('\t {0:>50s} {1:<70s} {2:>8} {3:>10s} {4:.10s} {5:.10s}'.format(c['project'], c['subject'],
                                                                                  c['_number'], c['status'],
                                                                                  c['created'], c['updated']))
        return openstack_person, len(changes)

    def print_launch_pad_bugs(self, openstack_person, start_date):
        bugs = lpbugsHelper.get_bugs_by_person(openstack_person, start_date)
        if bugs:
            print('\t{} {} {} {} {} {}'.format("=" * 20, "Launchpad bugs reported by: ", openstack_person,
                                               "=== Total Bugs: ", len(bugs), "=" * 20))
            print('\n')
            print('\t {0:>10} {1:>10} {2:>30} {3:>20}'.format("Reported By:", "Date Updated:", "Link:", "Title:"))
            for bug in bugs:
                print('\t {0:>10} {1:>10} {2:>15} {3:<.100}'.format(bug['author'], str(
                    datetime.fromtimestamp(mktime(bug['updated_parsed'])))[0:10], bug['link'], bug['title']))
        else:
            print("No recently opened LaunchPad bugs found")
        return openstack_person, len(bugs)

    def print_bugzilla_bugs(self, person, start_date):
        bugs = bzHelper.get_rhos_bugs(person, start_date)
        if bugs:
            print(
                '\t{} {} {} {} {} {}'.format("=" * 20, "Bugzilla bugs reported by: ", person, "=== Total Bugs: ",
                                             len(bugs), "=" * 20))
            print('\n')
            print('\t {0:>10} {1:>10} {2:>30} {3:>20}'.format("Status:", "Date Updated:", "Link:", "Title:"))
            for bug in bugs:
                print('\t {} {} {} {} '.format(bug.status, str(bug.last_change_time)[0:8], bug.weburl, bug.summary))
        else:
            print("No recently opened Bugzilla bugs found")
        return person, len(bugs)
