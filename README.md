This will print out a report with the following information:
* All recently modified trello cards across all boards in trello per person in
$TEAM

* All recent gerrit reviews in openstack or gerrithub that are in NEW or MERGED
  status

* All recent launchpad bugs opened by a person

* All recent bugzilla bugs opened by a person

Note: recent is configurable, but defaults to the last two weeks.

Requires:
python-feedparser
python-bugzilla

A TEAM variable must be set in environment.sh

Description:
export TEAM='{"red hat short name":{"trello":"trello user id", "rh_email":"whayutin@redhat.com", "openstack":"launchpad id",\
"gerrithub": "gerrithub id"}
}'

Example:
export TEAM='{"whayutin":{"trello":"weshayutin1", "rh_email":"whayutin@redhat.com", "openstack":"weshayutin",\
 "gerrithub":"weshayutin@gmail.com"}
}'

