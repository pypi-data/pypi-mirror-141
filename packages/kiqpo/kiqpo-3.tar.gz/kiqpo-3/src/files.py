from time import sleep, time
import zipfile
import requests
import os
from tqdm import tqdm
from color import colored
from config import config


def getfiles(json, appname="kiqpo", version="1.0.0", description="Using Kiqpo, we built this app", git_repository="www.github.com/kiqpo"):
    template_url = json[0]['assets'][0]['browser_download_url']
    template = requests.get(template_url, allow_redirects=True)
    # templateHeader = template.headers.get('content-length')
    # total_size_in_bytes = int(templateHeader)
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(unit='iB', unit_scale=True)
    with open(f'{appname}.zip', 'wb') as file:
        for data in template.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    with zipfile.ZipFile(f'{appname}.zip', 'r') as zip_ref:
        # extract zip files
        zip_ref.extractall('./')
        os.rename('kiqpo', f'{appname}')
        config_json = open(f'{os.getcwd()}/config.yaml', 'w+')
        config_json.write(config(appname=appname, version=version, description=description,
                          url=git_repository))

        # edit core.py
        with open(f'{os.getcwd()}/{appname}/core/core.py', 'r') as read:
            corePy = read.read()
        with open(f'{os.getcwd()}/{appname}/core/core.py', 'w+') as write:
            write.write(corePy.replace('kiqpo', appname))

        # edit kiqpo.py
        with open(f'{os.getcwd()}/{appname}/kiqpo.py', 'r') as readKiqpo:
            kiqpoPy = readKiqpo.read()
        with open(f'{os.getcwd()}/{appname}/kiqpo.py', 'w+') as writeKiqpo:
            writeKiqpo.write(kiqpoPy.replace('APPNAME', appname))

        # then remove zip file
        os.remove(f'{appname}.zip')
        print()
        print(colored(2, 119, 189, 'kiqpo run-web'))
        print()
        print(colored(124, 179, 66, 'Resulted in success!'))
