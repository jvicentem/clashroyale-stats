import csv

file_path = './clash-royale.csv'

with open(file_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)

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

    da_file_path = './clash-royale-da.csv'

    fields = (['my_result', 'my_score', 'points', 'opponent_score', 'my_trophies', 'opponent_trophies', 'opponent_has_clan', 'match_type']
                + op_cards + my_cards 
             )
    
    with open(da_file_path, 'w+') as csv_fileW:
        writer = csv.DictWriter(csv_fileW, dialect='excel', lineterminator='\n', fieldnames=fields)

        writer.writeheader()

        line = dict.fromkeys(fields, 0)

        next(reader)

        for row in reader:
            line['my_result'] = row['my_result']
            line['my_score'] = row['my_score']
            line['points'] = row['points']
            line['opponent_score'] = row['opponent_score']
            line['my_trophies'] = row['my_trophies']
            line['opponent_trophies'] = row['opponent_trophies']
            line['opponent_has_clan'] = row['opponent_has_clan']
            line['match_type'] = row['match_type']

            for i in list(range(1, 9)):
                line['my_' + row['my_card_%d' % i]] = row['my_card_%d_lvl' % i]

                for j in list(range(1, 9)):
                    if i != j:
                        line['my_' + row['my_card_%d' % j]] = 0

            for i in list(range(1, 9)):
                line['op_' + row['op_card_%d' % i]] = row['op_card_%d_lvl' % i]

                for j in list(range(1, 9)):
                    if i != j:
                        line['op_' + row['my_card_%d' % j]] = 0                

            writer.writerow(line)


