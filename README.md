There are a couple tools here.

#1 print_report.sh

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

    Please check the example-environment.sh for the required settings.
    A TEAM variable must be set in environment.sh

    Description:
    export TEAM='{"red hat short name":{"trello":"trello user id", "rh_email":"foo@redhat.com", "openstack":"launchpad id",\
    "gerrithub": "gerrithub id"}
    }'

#2 trello_due_dates.sh

    This will set cards with a due date if one is not already set. It defaults to 7 days from now.
    It will also print out a list of overdue cards.

    Check the example-environment.sh for the required settings.

