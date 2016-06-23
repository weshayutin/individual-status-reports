#!/usr/bin/python

import json
from datetime import datetime
from time import mktime

import feedparser
import requests
from dateutil.relativedelta import *

now = datetime.now()


class ApiContext():
    @property
    def launchpad_bug_feed(self):
        return "http://feeds.launchpad.net"

    @property
    def launchpad_api_root_url(self):
        return "https://api.launchpad.net/1.0"


class Bugs(object):
    def __init__(self, context):
        self._api = context

    def get_bugs_by_person(self, person=None, start_date=None):
        link = '{0}/{1}{2}/latest-bugs.atom'.format(self._api.launchpad_bug_feed, "~", person)
        data = feedparser.parse(link)
        all_bugs = data.entries
        bugs = []
        for bug in all_bugs:
            last_modified = datetime.fromtimestamp(mktime(bug['updated_parsed']))
            date = (now + relativedelta(weeks=start_date))
            if last_modified > date:
                if person in bug['author_detail']['href']:
                    bugs.append(bug)
        return bugs

    def get_bug_details(self, bugId):
        api_url = '{0}/bugs/{1}'.format(self._api.launchpad_api_root_url, bugId)
        response = requests.get(api_url)
        response.raise_for_status()
        jsonResponse = json.loads(response.text)
        return jsonResponse
