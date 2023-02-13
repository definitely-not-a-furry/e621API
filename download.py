import os
import json
from time import sleep
import requests

config=json.load(open('config.json',encoding='UTF-8'))
silent_mode = config['silent-mode']
debug_mode = config['debug-mode']
rate_limit = config['rate-limit']
path = config['path']

filenames = []

#url = "https://static1.e621.net/data/af/30/af30659e164e085c745814bf1174cafb.gif" # temporary testing link (cute fops :3)
urls = open('tmp\\links',encoding='utf-8').read().split('\n')

if urls == '':
    print('No posts found')
    os.system('pause')

def removeprefix(item):
    "removes first characters of the url i.e. https://static1/e621.net/af/34/"
    filename = item[29:]
    return filename

if not os.path.exists(path): # create folder if it does not exist
    os.makedirs(path)

for i in urls:
    file_path=(os.path.join(path,removeprefix(i)))
    try:
        r = requests.get(i, stream=True,timeout=10)
    except:
        raise Exception('Was unable to access file. Check if the website is accessible using a browser.')
    if r.ok:
        if silent_mode is False and debug_mode is False:
            print(i)
        elif debug_mode is True:
            print(f'Downloading "{i}" to "{file_path}"')
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print(f"Download failed: status code {r.status_code}\n{r.text}")
    sleep(rate_limit)
