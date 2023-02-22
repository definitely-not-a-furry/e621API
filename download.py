"Download files from links"
import json
import os
import sys
from time import sleep

import requests

with open('config.json',encoding='UTF-8') as f:
    config=json.load(f)

with open('tmp\\links',encoding='UTF-8') as f:
    urls=f.read().split('\n')

silent_mode=config['silent-mode']
debug_mode=config['debug-mode']
rate_limit=config['rate-limit']
path=config['path']

filenames=[]

class Download():
    "downloads files from urls"
    def __init__(self):
        if urls=='':
            print('No posts found')
            os.system('pause')
            print('exiting...')
            sys.exit()

        if not os.path.exists(path): #create folder if it does not exist
            os.makedirs(path)

        for i in urls:
            file_path=(os.path.join(path,self.removeprefix(i)))
            try:
                request=requests.get(i, stream=True,timeout=10)
            except ConnectionError as exc:
                raise ConnectionError('''Was unable to access file.
                Check if the website is accessible using a browser.''') from exc
            if request.ok:
                if silent_mode is False and debug_mode is False:
                    print(i)
                elif debug_mode is True:
                    print(f'Downloading "{i}" to "{file_path}"')
                with open(file_path, 'wb') as file:
                    for chunk in request.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            file.write(chunk)
                            file.flush()
                            os.fsync(file.fileno())
            else:
                print(f"Download failed: status code {request.status_code}\n{request.text}")
            if debug_mode:
                print(f'Sleeping for {rate_limit} second...')
            sleep(rate_limit)

    def removeprefix(self,item):
        "removes domain and directory from url"
        filename=item[29:]
        return filename
