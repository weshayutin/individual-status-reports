#!/usr/bin/python

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#import pdb

#
# API CONTEXT OBJECT
#
class ApiContext(object):
    @property
    def openstack_api_root_url(self):
        return "https://review.openstack.org"

    @property
    def gerrithub_api_root_url(self):
        return "https://review.gerrithub.io"

    @property
    def code_eng_root_url(self):
        return "https://code.engineering.redhat.com/gerrit"

    @property
    def rdoproject_root_url(self):
        return "https://review.rdoproject.org/r"
    


class Documentation(object):
    def __init__(self, context):
        self._api = context

    def get_doc(self):
        response = requests.get('{0}/Documentation/?q=test'.format(self._api.ApiRootUrl))
        response.raise_for_status()
        jsonResponse = json.loads(response.text[4:])
        return jsonResponse


class Changes(object):
    def __init__(self, context):
        self._api = context

    def get_open_changes_by_person(self, openstack_person, gerrithub_person, codeng_person, rdoproject_person, since_date):
        # get openstack.review.org changes
        s = '{0}/changes/?q=(status:open OR status:merged)+owner:{1}+after:{2}' \
            .format(self._api.openstack_api_root_url, openstack_person, since_date)
        response = requests.get(s)
        response.raise_for_status()
        openstack = json.loads(response.text[4:])

        # get gerrithub.review.org changes
        s = '{0}/changes/?q=(status:open+OR+status:merged)+owner:{1}+after:{2}' \
            .format(self._api.gerrithub_api_root_url, gerrithub_person, since_date)
        response = requests.get(s)
        response.raise_for_status()
        gerrithub = json.loads(response.text[4:])

        # get review.rdoproject changes
        s = '{0}/changes/?q=(status:open OR status:merged)+owner:{1}+after:{2}' \
            .format(self._api.rdoproject_root_url, rdoproject_person, since_date)
        response = requests.get(s)
        response.raise_for_status()
        rdoproject = json.loads(response.text[4:])

        # get code.engineering changes

        # turn off insecure warning for code.eng
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        s = '{0}/changes/?q=(status:open+OR+status:merged)+owner:{1}+after:{2}' \
            .format(self._api.code_eng_root_url, codeng_person, since_date)
        response = requests.get(s, verify=False)
        response.raise_for_status()
        codeng = json.loads(response.text[4:])

        # jsonResponse = {key: value for (key, value) in (openstack.items() + gerrithub.items())}
        jsonResponse = openstack + gerrithub + codeng + rdoproject

        return jsonResponse
