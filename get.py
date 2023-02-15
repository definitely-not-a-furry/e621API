"Request posts.json"
import os
import json
import sys
import requests

with open('config.json',encoding='UTF-8') as f:
    config = json.load(f)

header_name = config['header-name']
header_version = config['header-version']
username = config['username']
TAGS = sys.argv[1]
AMOUNT = sys.argv[2]
url=f"https://e621.net/posts.json?tags={TAGS}&limit={AMOUNT}"
headers = {'User-Agent': f'{header_name}/{header_version} (by {username})'}
print(url)

file = requests.get(url, headers=headers, timeout=10)

if os.path.exists('tmp\\posts.json'):
    os.system('del tmp\\posts.json')

if not config['silent-mode'] or config['debug-mode']:
    print(file)

file = file.json()

with open('tmp\\posts.json','w',encoding='UTF-8') as f:
    json.dump(file, f)

with open('tmp\\posts.json',encoding='UTF-8') as f:
    posts = json.load(f)

links = []

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

os.system('python download.py')
