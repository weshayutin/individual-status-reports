#!/usr/bin/env python

from datetime import datetime

import GerritToolbox as gerrit
import pytz
from dateutil.relativedelta import *

apiContext = gerrit.ApiContext()
# note: the only state kept in these is the context object
docHelper = gerrit.Documentation(apiContext)
changesHelper = gerrit.Changes(apiContext)

now = datetime.now(pytz.utc)


def list_reviews(person, from_weeks):
    date = (now + relativedelta(weeks=from_weeks)).strftime("%Y-%m-%d")
    changes = changesHelper.get_open_changes_by_person(person, date)
    print('\t {0:>50s} {1:<70s} {2:>8s} {3:>10s} {4:.10s} {5:.10s}'.format("project", "subject", "id", "status",
                                                                           "created", "   updated"))
    print("=" * 171)
    for c in changes:
        print('\t {0:>50s} {1:<70s} {2:>8} {3:>10s} {4:.10s} {5:.10s}'.format(c['project'], c['subject'], c['_number'],
                                                                              c['status'], c['created'], c['updated']))
    print(len(changes))


if __name__ == "__main__":
    print("========== List reviews for wes hayutin ==========")
    list_reviews('"weshayutin@gmail.com"', -2)
    print("========== List reviews for matt young ==========")
    list_reviews('"myoung@redhat.com"', -2)
