"Request posts.json"
import json
import os

import requests

import download

with open('config.json',encoding='UTF-8') as f:
    config=json.load(f)

header_name=config['header-name']
header_version=config['header-version']
username=config['username']

with open('tmp\\request',encoding='UTF-8') as f:
    f=f.split('\n')
    TAGS=f[0]
    AMOUNT=f[1]

URL=f"https://e621.net/posts.json?tags={TAGS}&limit={AMOUNT}"
headers={'User-Agent': f'{header_name}/{header_version} (by {username})'}
print(URL)

file=requests.get(URL, headers=headers, timeout=10)

if os.path.exists('tmp\\posts.json'):
    os.system('del tmp\\posts.json')

if not config['silent-mode'] or config['debug-mode']:
    print(file)

file=file.json()

with open('tmp\\posts.json','w',encoding='UTF-8') as f:
    json.dump(file, f)

with open('tmp\\posts.json',encoding='UTF-8') as f:
    posts=json.load(f)

links=[]

for i in posts['posts']:
    links.append(i['file']['url'])
    if config['debug-mode'] is True:
        print(i['file']['url'])

if not config['silent-mode'] or config['debug-mode']:
    print(f'Links: {str(links)}')

if os.path.exists('tmp\\links'):
    os.system('del tmp\\links')

with open('tmp\\links','w',encoding='UTF-8') as file:
    file.write('\n'.join(links))

download.Download()
