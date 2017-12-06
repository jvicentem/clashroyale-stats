from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
import re
import csv
import os
import USER_ID

class Crawler(CrawlSpider):
    name = 'crSpider'
    allowed_domains = ['statsroyale.com']
    start_urls = ['https://statsroyale.com/profile/' + USER_ID.USER_ID + '/battles']

    def parse(self, response):
        sel = Selector(response)        

        battles = sel.css('div[data-type="ranked"]')

        battles_objs = []

        for battle in battles:
            battle_obj = {}

            battle_obj['my_result'] = battle.css('div.replay__header > div.ui__headerExtraSmall::text')[0].extract()

            score = battle.css('div.replay__header > div.replay__record > div.replay__recordText.ui__headerExtraSmall::text')[0].extract()

            score = score.split('-')

            battle_obj['my_score'] = int(score[0])

            battle_obj['opponent_score'] = int(score[1])

            trophies = battle.css('div.replay__match div.replay__player > div.replay__playerName > div > div.replay__trophies::text').extract()            

            if not trophies:
                continue
                
            battle_obj['my_trophies'] = int(trophies[0])

            battle_obj['opponent_trophies'] = int(trophies[1])

            clans = battle.css('.replay__clanName::text').extract()

            battle_obj['i_have_clan'] = 'n' if 'No Clan' == clans[0].strip() else 'y'

            battle_obj['opponent_has_clan'] = 'n' if 'No Clan' == clans[1].strip() else 'y'

            battle_obj['match_type'] = battle.css('div.replay__header > div.replay__type > div::attr(class)')
            battle_obj['match_type'] = battle_obj['match_type'][0].extract() if len(battle_obj['match_type']) > 0 else 'replay__ladderBattleType'

            decks = battle.css('div.replay__match div.replay__player > div.replay__decklist')

            cards_my_deck = decks[0].css('a')

            battle_obj['my_deck'] = []

            for card in cards_my_deck:
                name = card.xpath('./@href')[0].extract()

                name = re.findall('/card/(.*)', name)[0].replace('+', '_')
                
                lvl = card.css('div > span::text')[0].extract()

                lvl = int(re.findall('Lvl (.*)', lvl)[0])

                battle_obj['my_deck'].append({'name': name, 'lvl': lvl})

            cards_opponent_deck = decks[1].css('a')

            battle_obj['opponent_deck'] = []

            for card in cards_opponent_deck:
                name = card.xpath('./@href')[0].extract()

                name = re.findall('/card/(.*)', name)[0].replace('+', '_')
                
                lvl = card.css('div > span::text')[0].extract()

                lvl = int(re.findall('Lvl (.*)', lvl)[0])             

                battle_obj['opponent_deck'].append({'name': name, 'lvl': lvl})   

            points = battle.css('div.replay__date::text')[0].extract()
            points = points.strip().split('•')
            battle_obj['points'] = int(points[0]) if len(points) > 1 else 0

            battles_objs.append(battle_obj)

        file_path = './' + USER_ID.USER_ID + '-clash-royale.csv'

        try:
            csv_file_r = open(file_path, 'r')
            reader = csv.DictReader(csv_file_r)
            newest_battle_in_csv = next(reader)            
        except FileNotFoundError:
            csv_file_r = None

        aux_file_path = './clash-royale-aux.csv'

        with open(aux_file_path, 'w+') as csv_file:
            fields = (['my_result', 'my_score', 'points', 'opponent_score', 
                'my_trophies', 'opponent_trophies', 'i_have_clan', 'opponent_has_clan', 'match_type',
                'my_card_1', 'my_card_1_lvl', 'my_card_2', 'my_card_2_lvl', 'my_card_3', 'my_card_3_lvl', 
                'my_card_4', 'my_card_4_lvl', 'my_card_5', 'my_card_5_lvl', 'my_card_6','my_card_6_lvl', 
                'my_card_7', 'my_card_7_lvl', 'my_card_8','my_card_8_lvl',
                'op_card_1', 'op_card_1_lvl', 'op_card_2', 'op_card_2_lvl', 'op_card_3', 'op_card_3_lvl', 
                'op_card_4', 'op_card_4_lvl', 'op_card_5', 'op_card_5_lvl', 'op_card_6','op_card_6_lvl', 
                'op_card_7', 'op_card_7_lvl', 'op_card_8','op_card_8_lvl'])

            writer = csv.DictWriter(csv_file, dialect="excel", lineterminator='\n', fieldnames=fields)

            writer.writeheader()

            for battle_obj in battles_objs:                
                row = {
                    'my_result': battle_obj['my_result'],
                    'my_score': battle_obj['my_score'],
                    'points': battle_obj['points'],
                    'opponent_score': battle_obj['opponent_score'],
                    'my_trophies': battle_obj['my_trophies'],
                    'opponent_trophies': battle_obj['opponent_trophies'],
                    'i_have_clan': battle_obj['i_have_clan'],
                    'opponent_has_clan': battle_obj['opponent_has_clan'],
                    'match_type': battle_obj['match_type']
                }

                for i, card in enumerate(battle_obj['my_deck']):
                    number = i + 1
                    row['my_card_%d' % number] = card['name']
                    row['my_card_%d_lvl' % number] = card['lvl']

                for i, card in enumerate(battle_obj['opponent_deck']):
                    number = i + 1
                    row['op_card_%d' % number] = card['name']
                    row['op_card_%d_lvl' % number] = card['lvl']                

                if csv_file_r:
                    if not newest_battle_in_csv == row:
                        writer.writerow(row)
                    else:
                        break
                else:
                    writer.writerow(row)

            if csv_file_r:
                for row in reader:
                    writer.writerow(row)

                os.remove(file_path)

            os.rename(aux_file_path, file_path)

            if csv_file_r:
                csv_file_r.close()
