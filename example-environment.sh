export trello_token="token"
export trello_api_key="api_key"
export BZ_USER=
export BZ_PASSWORD=
export RECENT="-2" #Number of weeks from now.  e.g two weeks ago

#key = Red Hat short name
#trello = Trello Member Name
#rh_email = Red Hat email
#openstack = launchpad account email address
#gerrithub = gerrithub account email address
export TEAM='{"whayutin":{"trello":"weshayutin1", "rh_email":"foo@redhat.com", "openstack":"foo@gmail.com", "gerrithub":"foo@gmail.com"},
}'

# Trello Card Due Dates
export BOARD_TO_CHECK="Board Name"
export BOARD_TO_CHECK_ID="hash"  #get hash by http://trello.com/b/board.json
export BOARD_TO_CHECK_COLUMN="In Progress"
export MY_TRELLO_ID="weshayutin1"
export OVERDUE_NOTICE="This card is overdue, please review https://etherpad.openstack.org/p/uETabgwn3P"
export BLOCKING_LABELS="['BLOCKED', 'WAIT FOR REVIEW or MERGE']"
export TRELLO_BOARD_BLACKLIST="hash"
