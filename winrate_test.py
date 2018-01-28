import requests
import time
import xml.etree.cElementTree

play_count = 0
win_count = 0

rate_delay = 0.6

records_per_page = 100
#game_id = 161936
game_id = 171668

start_time = time.time()

payload = {'id': game_id, 'page': 1}
query = requests.get("https://www.boardgamegeek.com/xmlapi2/plays?", params=payload)
element_tree = xml.etree.cElementTree.fromstring(query.content)

print(element_tree.tag, element_tree.attrib)
pages_of_records = int(int(element_tree.attrib['total'])/records_per_page) + 1

# Python 3 has no xrange, range == Python2's xrange. Python2's range no longer exists
for i in range(pages_of_records):
    payload = {'id': game_id, 'page': i}
    query = requests.get("https://www.boardgamegeek.com/xmlapi2/plays?", params=payload)
    element_tree = xml.etree.cElementTree.fromstring(query.content)

    for item in element_tree:
        #print(item.tag, item.attrib)

        # Skip incomplete plays
        if 'incomplete' not in item.attrib:
            continue
        if not item.attrib['incomplete']:
            continue
        players = item.find('players')
        if players:
            # Players are located, so enough play data is found, log a play
            play_count += 1
            num_of_winners = 0
            for player in players:
                if player.attrib['win'] == "1":
                    num_of_winners += 1
                #print(player.attrib['win'])
            #print("playerlen", len(players))
            #print('numwin', num_of_winners)
            if num_of_winners >= len(players):
                win_count += 1
    print("Page: ", i)
    if play_count != 0:
        print("Current winrate: ", (win_count / play_count))
    time.sleep(rate_delay)

print(win_count)
print(play_count)
if play_count != 0:
    print(win_count/play_count)

print("Process took: ", time.time()-start_time)
