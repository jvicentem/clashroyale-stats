import csv
import CARDS_INFO
import numpy as np
import USER_ID_DEV

file_path = './ClashRoyale/' + USER_ID_DEV.USER_ID + '-clash-royale.csv'

with open(file_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)

    my_decks_elixir = []
    op_decks_elixir = [] 
    for row in reader:
        my_cards_elixir = []
        for i in range(1, 9):
            my_cards_elixir.append(CARDS_INFO.CARDS[row['my_card_' + str(i)]]['elixir'])

        op_cards_elixir = []
        for i in range(1, 9):
            op_cards_elixir.append(CARDS_INFO.CARDS[row['op_card_' + str(i)]]['elixir'])            

        my_decks_elixir.append(np.mean(my_cards_elixir))
        op_decks_elixir.append(np.mean(op_cards_elixir))

    csv_file.seek(0)
    next(reader)

    my_decks_types = []
    op_decks_types = [] 
    for row in reader:
        my_troop_count = 0
        my_building_count = 0
        my_spell_count = 0

        for i in range(1, 9):
            if CARDS_INFO.CARDS[row['my_card_' + str(i)]]['type'] == 'Troop':
                my_troop_count += 1
            elif CARDS_INFO.CARDS[row['my_card_' + str(i)]]['type'] == 'Building':
                my_building_count += 1
            else:
                my_spell_count += 1

        my_decks_types.append({'Troop': my_troop_count, 'Building': my_building_count, 'Spell': my_spell_count})

        op_troop_count = 0
        op_building_count = 0
        op_spell_count = 0

        for i in range(1, 9):
            if CARDS_INFO.CARDS[row['op_card_' + str(i)]]['type'] == 'Troop':
                op_troop_count += 1
            elif CARDS_INFO.CARDS[row['op_card_' + str(i)]]['type'] == 'Building':
                op_building_count += 1
            else:
                op_spell_count += 1

        op_decks_types.append({'Troop': op_troop_count, 'Building': op_building_count, 'Spell': op_spell_count})    

    csv_file.seek(0)
    next(reader)    

    my_decks_rarities = []
    op_decks_rarities = [] 
    for row in reader:
        my_common_count = 0
        my_rare_count = 0
        my_epic_count = 0
        my_legendary_count = 0

        for i in range(1, 9):
            if CARDS_INFO.CARDS[row['my_card_' + str(i)]]['rarity'] == 'Common':
                my_common_count += 1
            elif CARDS_INFO.CARDS[row['my_card_' + str(i)]]['rarity'] == 'Rare':
                my_rare_count += 1
            elif CARDS_INFO.CARDS[row['my_card_' + str(i)]]['rarity'] == 'Epic':
                my_epic_count += 1
            else:
                my_legendary_count += 1

        my_decks_rarities.append({'Common': my_common_count, 'Rare': my_rare_count, 'Epic': my_epic_count, 'Legendary': my_legendary_count})

        op_common_count = 0
        op_rare_count = 0
        op_epic_count = 0
        op_legendary_count = 0

        for i in range(1, 9):
            if CARDS_INFO.CARDS[row['op_card_' + str(i)]]['rarity'] == 'Common':
                op_common_count += 1
            elif CARDS_INFO.CARDS[row['op_card_' + str(i)]]['rarity'] == 'Rare':
                op_rare_count += 1
            elif CARDS_INFO.CARDS[row['op_card_' + str(i)]]['rarity'] == 'Epic':
                op_epic_count += 1
            else:
                op_legendary_count += 1

        op_decks_rarities.append({'Common': op_common_count, 'Rare': op_rare_count, 'Epic': op_epic_count, 'Legendary': op_legendary_count})

    csv_file.seek(0)
    next(reader)        

    op_cards = list()
    my_cards = list()

    for row in reader:
        op_cards.append('op_' + row['op_card_1'])
        op_cards.append('op_' + row['op_card_2'])
        op_cards.append('op_' + row['op_card_3'])
        op_cards.append('op_' + row['op_card_4'])
        op_cards.append('op_' + row['op_card_5'])
        op_cards.append('op_' + row['op_card_6'])
        op_cards.append('op_' + row['op_card_7'])
        op_cards.append('op_' + row['op_card_8'])

        my_cards.append('my_' + row['my_card_1'])
        my_cards.append('my_' + row['my_card_2'])
        my_cards.append('my_' + row['my_card_3'])
        my_cards.append('my_' + row['my_card_4'])
        my_cards.append('my_' + row['my_card_5'])
        my_cards.append('my_' + row['my_card_6'])
        my_cards.append('my_' + row['my_card_7'])
        my_cards.append('my_' + row['my_card_8'])

    op_cards = list(set(op_cards))
    my_cards = list(set(my_cards))

    csv_file.seek(0)

    da_file_path = './' + USER_ID_DEV.USER_ID + '-clash-royale-da.csv'

    fields = (['my_result', 'my_score', 'points', 'opponent_score', 'my_trophies', 'opponent_trophies', 'i_have_clan', 'opponent_has_clan', 'match_type', 
               'my_deck_elixir', 'op_deck_elixir', 'my_troops', 'my_buildings', 'my_spells', 'op_troops', 'op_buildings', 'op_spells', 'my_commons', 'my_rares',
               'my_epics', 'my_legendaries', 'op_commons', 'op_rares', 'op_epics', 'op_legendaries']
                + op_cards + my_cards 
             )
    
    with open(da_file_path, 'w+') as csv_fileW:
        writer = csv.DictWriter(csv_fileW, dialect='excel', lineterminator='\n', fieldnames=fields)

        writer.writeheader()

        line = dict.fromkeys(fields, 0)

        next(reader)

        for i, row in enumerate(reader):
            line['my_result'] = row['my_result']
            line['my_score'] = row['my_score']
            line['points'] = row['points']
            line['opponent_score'] = row['opponent_score']
            line['my_trophies'] = row['my_trophies']
            line['opponent_trophies'] = row['opponent_trophies']
            line['i_have_clan'] = row['i_have_clan']
            line['opponent_has_clan'] = row['opponent_has_clan']
            line['match_type'] = row['match_type']
            line['my_deck_elixir'] = my_decks_elixir[i]
            line['op_deck_elixir'] = op_decks_elixir[i]    
            line['my_troops'] = my_decks_types[i]['Troop']
            line['my_buildings'] = my_decks_types[i]['Building']
            line['my_spells'] = my_decks_types[i]['Spell']
            line['op_troops'] = op_decks_types[i]['Troop']
            line['op_buildings'] = op_decks_types[i]['Building']
            line['op_spells'] = op_decks_types[i]['Spell']     
            line['my_commons'] = my_decks_rarities[i]['Common']       
            line['my_rares'] = my_decks_rarities[i]['Rare']       
            line['my_epics'] = my_decks_rarities[i]['Epic']       
            line['my_legendaries'] = my_decks_rarities[i]['Legendary']   
            line['op_commons'] = op_decks_rarities[i]['Common']       
            line['op_rares'] = op_decks_rarities[i]['Rare']       
            line['op_epics'] = op_decks_rarities[i]['Epic']       
            line['op_legendaries'] = op_decks_rarities[i]['Legendary']                   

            for i in list(range(1, 9)):
                line['my_' + row['my_card_%d' % i]] = row['my_card_%d_lvl' % i]

                for j in list(range(1, 9)):
                    if i != j:
                        line['my_' + row['my_card_%d' % j]] = 0

            for i in list(range(1, 9)):
                line['op_' + row['op_card_%d' % i]] = row['op_card_%d_lvl' % i]

                for j in list(range(1, 9)):
                    if i != j:
                        line['op_' + row['op_card_%d' % j]] = 0                

            writer.writerow(line)
