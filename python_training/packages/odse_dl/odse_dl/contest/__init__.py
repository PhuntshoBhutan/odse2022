import requests
import json
import rasterio as rio
import numpy as np
import os
from pathlib import Path
from typing import Union
import shutil

# BASE_URL = 'http://127.0.0.1:5000/'
BASE_URL = 'https://kepler.multione.hr/odse2022/'
CWD = Path(os.getcwd())
AUTH_FILE = CWD / 'odse2022_contest_credentials.json'

try:
    from google.colab import drive as _drive
except (ModuleNotFoundError, ImportError):
    _drive = None

class drive:

    @staticmethod
    def store_credentials():
        _drive.mount('/content/drive')
        shutil.copy(
            AUTH_FILE,
            Path('/content/drive/MyDrive')/AUTH_FILE.name,
        )

    @staticmethod
    def retrieve_credentials():
        _drive.mount('/content/drive')
        shutil.copy(
            Path('/content/drive/MyDrive')/AUTH_FILE.name,
            AUTH_FILE,
        )

def get_creds(
    verbose: bool=True,
) -> Union[dict, None]:
    try:
        with open(AUTH_FILE) as src:
            return json.load(src)
    except FileNotFoundError:
        if verbose:
            print(
                'Contestant credentials not found, please register.',
                f'If you have already registered, run this code from a directory containing {AUTH_FILE.name}',
                '\nIf you have previously stored credentials from Google Colab to Drive, try running:',
                'contest.drive.retrieve_credentials()',
            sep='\n')
        return None

def register(
    name: str,
) -> str:
    creds = get_creds(verbose=False)
    if creds is not None:
        print(
            f'You are already registered as {creds["name"]}',
        )
        return

    resp = requests.post(
        BASE_URL+'register',
        data=json.dumps({
            'name': name,
        })
    )
    if resp.status_code == 406:
        print(f'Name {name} is already taken.')
    elif resp.status_code == 200:
        data = resp.json()
        with open(AUTH_FILE, 'w') as dst:
            json.dump(data, dst, indent=4)
        print(
            f'Thanks for participating, {name}!',
            f'Credentials saved to {AUTH_FILE}',
            f'Your token is {data["token"]}',
        sep='\n')
        return data['token']

def rebuild_credentials(
    token: str,
):
    creds = get_creds(verbose=False)
    if creds is not None:
        print(
            f'Credentials file found: {AUTH_FILE}',
        )
        return

    resp = requests.post(
        BASE_URL+'retrieve_credentials',
        data=json.dumps({
            'token': token,
        })
    )
    if resp.status_code == 403:
        print(f'Invalid token.')
    elif resp.status_code == 200:
        data = resp.json()
        with open(AUTH_FILE, 'w') as dst:
            json.dump(data, dst, indent=4)
        print(
            f'Credentials retrieved and saved to {AUTH_FILE}',
        sep='\n')

def submit(
    data: Union[np.ndarray, Path, str],
):

    creds = get_creds()
    if creds is None:
        return

    if isinstance(data, (Path, str)):
        with rio.open(data) as src:
            data = src.read(1)

    shape = np.array(data.shape)
    if shape.size > 2:
        data = data.reshape(shape[shape>1])

    resp = requests.post(
        BASE_URL+'submit',
        data=json.dumps({
            'name': creds['name'],
            'token': creds['token'],
            'data': data.tolist(),
        })
    )

    if resp.status_code == 429:
        print(
            'Submition rate is limited to once in 5 minutes.',
            'Please try again later.',
        sep='\n')

    else:
        print(resp.text)

def scoreboard():
    resp = requests.get(BASE_URL+'scoreboard')
    print(resp.text)
