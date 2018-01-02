# -*- coding: utf-8 -*-
"""This Python script aims to retrieve battles info of multiple
Clash Royale player profile to perform data analysis in the future.
"""

import requests

CR_API_TOKEN = ''

PLAYERS_TAGS = []

def request_user_info(user_id):
    headers = {"auth": CR_API_TOKEN}
    url = 'http://api.cr-api.com/player/' + user_id
    response = requests.get(url, headers=headers)
    return response.json()

def deal_with_battle(battle_dict):
    line = {}

    line['my_score'] = battle_dict['teamCrowns']

    line['opponent_score'] = battle_dict['opponentCrowns']

    line['my_result'] = ('Victory' if line['my_score'] > line['opponent_score'] 
                        else 
                        'Defeat' if line['my_score'] < line['opponent_score'] 
                        else 'Draw')

    line['points'] = # Currently the api doesn't retrieve the number of trophies earned per battle
                     #so the cr-api migration development stops here until further notice



#################################################################################################

for user_tag in PLAYERS_TAGS:
    file_path = './' + user_tag + '-clash-royale.csv'

    user_response = request_user_info(user_tag)

    battles = user_response['battles']

    lines = []

    for battle in battles:
        lines.append(deal_with_battle(battle))
        