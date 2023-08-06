import os
import yaml


def runWeb():
    with open(f'{os.getcwd()}/config.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)
        file_path = prime_service['paths']['kiqpo']
    fullpath = f'{os.getcwd()}{file_path}'
    os.system('{} {}'.format('python3', f'{fullpath} run-web'))

