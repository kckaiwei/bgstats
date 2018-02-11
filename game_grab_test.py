import requests
import time
import xml.etree.cElementTree

game_id = 161936

payload = {'id': game_id}
query = requests.get('https://www.boardgamegeek.com/xmlapi2/thing?', params=payload)
element_tree = xml.etree.cElementTree.fromstring(query.content)
for item in element_tree:
    print(item.find('maxplayers').attrib['value'])

    names = item.findall('name')
    if not names:
        pass
    # Backup, set as first name, usually primary
    #game_name = names[0].attrib['value']
    for name in names:
        if 'type' in name.attrib:
            if name.attrib['type'] == 'primary':
                game_name = name.attrib['value']
        print(name.attrib['value'])
    print('final_name:', game_name)
