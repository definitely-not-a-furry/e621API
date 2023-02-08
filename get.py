import requests, os, json, sys

config = json.load(open('config.json'))
tags = sys.argv[1]
amount = sys.argv[2]
url=f"https://e621.net/posts.json?tags={tags}&limit={amount}"
headers = {'User-Agent': 'test_project/none (by deeznu)'}
print(url)

file = requests.get(url, headers=headers)

if os.path.exists('tmp\\posts.json'):
    os.system('del tmp\\posts.json')

if not config['silent-mode'] or config['debug-mode']:
    print(file)

file = file.json()

with open('tmp\\posts.json','w') as f:
    json.dump(file, f)

posts = json.load(open('tmp\\posts.json'))
config = json.load(open('config.json'))
links = list()

for i in posts['posts']:
    links.append(i['file']['url'])
    if config['debug-mode'] == True:
        print(i['file']['url'])

if config['silent-mode'] == False or config['debug-mode'] == True:
    print(f'Links: {str(links)}')

if os.path.exists('tmp\\links'):
    os.system('del tmp\\links')

with open('tmp\\links', 'w') as file:
    file.write('\n'.join(links))

os.system('python download.py')