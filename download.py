import os, requests, json

configfile = open('config.json',) # load configuration file
config=json.load(configfile)
silent_mode = config['silent-mode']
debug_mode = config['debug-mode']

filenames = []

#url = "https://static1.e621.net/data/af/30/af30659e164e085c745814bf1174cafb.gif" # temporary testing link
urls = open('tmp\\links').read().split('\n')

if urls == '':
    print('No posts found')
    os.system('pause')

def removeprefix(item):
    filename = item.replace('https://static1.e621.net/data/', '')
    filename = filename[filename.find('/'):]
    filename = filename[1:]
    filename = filename[filename.find('/'):]
    filename = filename[1:]
    return(filename)

if not os.path.exists('out'): # create folder if it does not exist
    os.makedirs('out')

for i in urls:
    file_path=(os.path.join('out',removeprefix(i)))
    try:
        r = requests.get(i, stream=True)
    except:
        raise Exception('Exeption: was unable to access file. Check if you can access the website using a browser.')
    if r.ok:
        if silent_mode == False and debug_mode == False:
            print(i)
        elif debug_mode == True:
            print(f'Downloading "{i}" to "{file_path}"')
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
