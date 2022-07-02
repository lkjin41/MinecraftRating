import time

import requests
from bs4 import BeautifulSoup as bs
import json

servers_file = open('servers.txt', 'w', encoding='utf-8')
num = 1

with open('urls.txt', 'r') as uf:
    while True:
        line = uf.readline()
        if not line:
            break
        r = requests.get(line.strip())
        print(str(r.status_code) + f'[{line.strip()}]' + "\033[32m{}".format(int))
        soup = bs(r.text, 'html.parser')
        name = soup.find("h1", {"itemprop": "name"}).text
        desc = soup.find("div", {"class": "description"}).text
        lure = soup.find("div", {"class": "slogan"}).text
        launcher_url = None
        ip_address = None
        url_address = None
        players_online = None
        players_max = None
        website = None
        vk = None
        discord = None
        version = str
        tags = []
        minecraftratingru_url = line.strip()
        trs = soup.find_all('tr')

        for tr in trs:
            if 'IP адрес:' in tr.text:
                if 'Только через лаунчер ' in tr.text:
                    launcher_btn = tr.find('a')
                    spl1 = launcher_btn['onclick'].split('//')
                    spl2 = spl1[1].split("'))")
                    launcher_url = spl2[0]
                else:
                    ip_address = tr.find('kbd', {'class': 'tooltip'}).text
                    for c in list(tr.find('kbd', {'class': 'tooltip'}).text):
                        if c.isalpha() is True:
                            url_address = tr.find('kbd', {'class': 'tooltip'}).text
                            ip_address = ''
                            break
                        else:
                            continue
            elif 'Игроков онлайн:' in tr.text:
                players_online = tr.find('strong').text.split(' из ')[0]
                players_max = tr.find('strong').text.split(' из ')[1]
            elif 'Был онлайн:' in tr.text:
                last_online = tr.find_all('td')[1].text
            elif 'Сайт сервера:' in tr.text:
                web_btn = tr.find('a')
                spl1 = web_btn['onclick'].split('//')
                spl2 = spl1[1].split("'))")
                website = spl2[0]
            elif 'Группа сервера в ВК:' in tr.text:
                vk_btn = tr.find('a')
                spl1 = vk_btn['onclick'].split('//')
                spl2 = spl1[1].split("'))")
                vk = spl2[0]
            elif 'Discord:' in tr.text:
                dis_btn = tr.find('a')
                spl1 = dis_btn['onclick'].split('//')
                spl2 = spl1[1].split("'))")
                discord = spl2[0]
            elif 'Версия:' in tr.text:
                version = tr.find('a').text

        for tag in soup.find_all('a', {'class': 'label-default'}):
            tags.append(tag.text)

        server_info = {'name': name,
                       'description': desc,
                       'lure': lure,
                       'launcher_url': launcher_url,
                       'ip_address': ip_address,
                       'url_address': url_address,
                       'players_online': players_online,
                       'players_max': players_max,
                       'website': website,
                       'vk': vk,
                       'discord': discord,
                       'version': version,
                       'minecraft_rating_url': minecraftratingru_url,
                       'tags': tags}

        json.dump(server_info, servers_file, ensure_ascii=False)
        servers_file.write(', ')
        num += 1
servers_file.close()
