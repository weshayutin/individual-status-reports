#!/usr/bin/env python3

import ast
import os
from datetime import datetime

import TrelloToolbox as trello
import pdb
import pytz
from dateutil.relativedelta import *

# Global variables
now = datetime.now(pytz.utc)


_myToken = os.environ.get('trello_token')

apiContext = trello.ApiContext(_myToken)
boardsHelper = trello.Boards(apiContext)
cardsHelper = trello.Cards(apiContext)
membersHelper = trello.Members(apiContext)


def print_cards(cards, header=""):
    "Print a list of cards in a nice neat summary view"
    if cards:
        print(header)
        print('\t {} {} {} {}'.format("Card Name", "Due Date", "Card Member", "Card Short Link"))
        for c in cards:
            print('\t {} {} {} {}'.format(c['name'], c['due'][0:10],
                                          membersHelper.get_member_names_from_list(c['idMembers']), c['url']))
    else:
        print("No Overdue Cards Found")


def set_trello_due_date(team, board_name, trello_user, column_name, blocking_labels, overdue_notice):
    boardId = boardsHelper.get_single_by_member_and_name(trello_user, board_name)
    member_list = [membersHelper.get_member_id(team[member]['trello']) for member in team]
    listId = boardsHelper.get_single_list_by_name(boardId, column_name)

    card_list = []
    card_list = cardsHelper.get_cards(listId)
    overdue_cards = []

    in_one_week = now + relativedelta(weeks=+1)
    in_one_week = in_one_week.strftime('%Y-%m-%dT%H:%M:%S')
    # print(in_one_week)
    for card in card_list:
        if card['idMembers']:
            if card['idMembers'] is not None:
                if listId == card['idList']:
                    if card['due'] is None:
                        cardsHelper.add_due_date_to_card(card, in_one_week)
                    if card['due'] is not None:
                        if cardsHelper.check_card_overdue(card['id'], blocking_labels, overdue_notice):
                            overdue_cards.append(card)

        else:
            cardsHelper.add_comment_to_card(card['id'], "Please add a member to this card")

    return overdue_cards

if __name__ == "__main__":
    team = ast.literal_eval(os.environ['TEAM'])
    board_to_check = os.environ['BOARD_TO_CHECK']
    board_to_check_column = os.environ.get('BOARD_TO_CHECK_COLUMN')
    my_trello_id = os.environ.get('MY_TRELLO_ID')
    overdue_notice = os.environ.get('OVERDUE_NOTICE')
    blocking_labels = ast.literal_eval(os.environ['BLOCKING_LABELS'])

    print_cards(set_trello_due_date(team, board_to_check, my_trello_id, board_to_check_column, blocking_labels, overdue_notice), "Overdue Card List:")
