import pytest
from checker_seminar3 import checkout_positive
import random
import string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout_positive(f'mkdir {data["test"]} {data["folder_e"]} {data["folder_x"]} {data["folder_broken"]}', '')


@pytest.fixture(autouse=True)
def clear_folders():
    checkout_positive(
        f'rm -rf {data["test"]} {data["out"]} {data["folder_e"]} {data["folder_x"]} {data["folder_broken"]}', '')
    yield


@pytest.fixture()
def make_files():
    list_of_files = []

    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.txt'
        if checkout_positive(f'cd {data["test"]}; dd if=/dev/urandom of={filename} bs={data["bs"]} '
                             f'count={data["count"]} iflag=fullblock', ''):
            list_of_files.append(filename)

    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    if not checkout_positive(f'cd {data["test"]}; mkdir {subfoldername}', ''):
        return None, None
    if not checkout_positive(f'cd {data["test"]}/{subfoldername}; dd if=/dev/urandom of={testfilename} '
                             f'bs={data["bs"]} count={data["count"]} iflag=fullblock', ''):
        return subfoldername, None

    return subfoldername, testfilename


@pytest.fixture()
def create_corrupted_archive():
    '''Создание битого архива'''
    checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok')
    checkout_positive(f'cp {data["out"]}/arx2.7z {data["folder_broken"]}', '')
    checkout_positive(f'truncate -s 1 {data["folder_broken"]}/arx2.7z', '')


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
