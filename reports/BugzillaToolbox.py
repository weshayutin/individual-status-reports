#!/usr/bin/python

import os
from datetime import datetime

import bugzilla
from dateutil.relativedelta import *

now = datetime.now()

bz = bugzilla.Bugzilla(url='https://bugzilla.redhat.com/xmlrpc.cgi')
bz.login(os.environ['BZ_USER'], os.environ['BZ_PASSWORD'])

REDHAT_OPENSTACK = "https://bugzilla.redhat.com/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=POST&\
bug_status=MODIFIED&bug_status=ON_DEV&bug_status=ON_QA&bug_status=VERIFIED&\
bug_status=RELEASE_PENDING&bug_status=CLOSED&classification=Red%20Hat&\
emailreporter1=1&emailtype1=exact&known_name=RHEL%20OSP%20Director%20Triage&\
list_id=3921001&product=Red%20Hat%20OpenStack&query_based_on=RHEL%20OSP%20Director%20Triage&query_format=advanced&\
chfieldfrom=REPLACE_DATE&chfieldto=Now&\
email1=REPLACE_PERSON%40redhat.com"

RDO_OPENSTACK = "https://bugzilla.redhat.com/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=POST&\
bug_status=MODIFIED&bug_status=ON_DEV&bug_status=ON_QA&bug_status=VERIFIED&\
bug_status=RELEASE_PENDING&bug_status=CLOSED&classification=Community&\
emailreporter1=1&emailtype1=exact&\
list_id=3921001&product=RDO&query_format=advanced&\
chfieldfrom=REPLACE_DATE&chfieldto=Now&\
email1=REPLACE_PERSON%40redhat.com"


# API CONTEXT OBJECT
class ApiContext():
    @property
    def foo(self):
        return "bar"


#
# BOARDS
#
class Bugs(object):
    def __init__(self, context):
        self._api = context

    # note: it's not currently possible to nuke a board, only to close it
    def get_rhos_bugs(self, username, start_date):
        "test the query"
        date = (now + relativedelta(weeks=start_date)).strftime("%Y-%m-%d")
        query = REDHAT_OPENSTACK.replace("REPLACE_PERSON", username)
        query = query.replace("REPLACE_DATE", date)
        #   print(query)
        rh_openstack_bug_list = bz.query(bz.url_to_query(query))
        query = RDO_OPENSTACK.replace("REPLACE_PERSON", username)
        query = query.replace("REPLACE_DATE", date)
        rdo_openstack_bug_list = bz.query(bz.url_to_query(query))

        bug_list = rh_openstack_bug_list + rdo_openstack_bug_list
        return bug_list
