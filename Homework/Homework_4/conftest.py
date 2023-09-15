import paramiko
import pytest
import random
import string
import yaml
from paramiko import SSHClient
from sshcheckers import ssh_checkout
from datetime import datetime
from typing import Any, Generator

with open('config.yaml') as f:
    data: Any = yaml.safe_load(f)


@pytest.fixture()
def make_folders() -> bool:
    '''Создание директорий'''
    return ssh_checkout(data['ip'], data['user'], data['passwd'],
                        f'mkdir {data["test"]} {data["folder_e"]} {data["folder_x"]} {data["folder_broken"]}', '', True)


@pytest.fixture(autouse=True)
def clear_folders() -> None:
    '''Удаление директорий'''
    ssh_checkout(data['ip'], data['user'], data['passwd'],
                 f'rm -rf {data["test"]} {data["out"]} {data["folder_e"]} {data["folder_x"]} {data["folder_broken"]}',
                 '', True)


@pytest.fixture()
def make_files() -> list[str]:
    '''Создание файлов'''
    list_of_files: list[str] = []

    for i in range(data["count"]):
        filename: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.txt'
        if ssh_checkout(data['ip'], data['user'], data['passwd'],
                        f'cd {data["test"]}; dd if=/dev/urandom of={filename} bs={data["bs"]} count={data["count"]} '
                        f'iflag=fullblock', '', True):
            list_of_files.append(filename)

    return list_of_files


@pytest.fixture()
def make_subfolder() -> tuple:
    '''Создание поддиректорий с файлами'''
    testfilename: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.txt'
    subfoldername: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    if not ssh_checkout(data['ip'], data['user'], data['passwd'], f'cd {data["test"]}; mkdir {subfoldername}', '',
                        True):
        return None, None

    if not ssh_checkout(data['ip'], data['user'], data['passwd'],
                        f'cd {data["test"]}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs={data["bs"]} '
                        f'count={data["count"]} iflag=fullblock', '', True):
        return subfoldername, None

    return subfoldername, testfilename


@pytest.fixture()
def create_corrupted_archive() -> None:
    '''Создание битого архива'''
    ssh_checkout(data['ip'], data['user'], data['passwd'],
                 f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}', 'Everything is Ok', True)
    ssh_checkout(data['ip'], data['user'], data['passwd'],
                 f'cp {data["out"]}/arx2.{data["archive_type"]} {data["folder_broken"]}', '', True)
    ssh_checkout(data['ip'], data['user'], data['passwd'],
                 f'truncate -s 1 {data["folder_broken"]}/arx2.{data["archive_type"]}', '', True)


@pytest.fixture(autouse=True)
def print_time() -> Generator[Any, Any, None]:
    '''Вывод времени начала и окончания выполнения теста'''
    print(f"Начало: {datetime.now().strftime('%H:%M:%S')}")
    yield
    print(f"\nОкончание: {datetime.now().strftime('%H:%M:%S')}")


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True)
def collect_statistics_for_test(request, port=22) -> None:
    '''Создание файла со статистикой, с внесением информации в этот файл'''
    test_start_time: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    test_name: Any = request.node.name
    class_name: str = request.cls.__name__ if request.cls else ""

    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(data['ip'], username=data['user'], password=data['passwd'], port=port)

    stdin, stdout, stderr = ssh_client.exec_command('cat /proc/loadavg')
    current_cpu_load: Any = stdout.read().decode('utf-8').strip()

    with open('test_statistics.txt', 'a', encoding='utf-8') as stat_file:
        stat_file.write(f'Время запуска: {test_start_time}; '
                        f'Название класса: {class_name}; '
                        f'Название теста: {test_name}; '
                        f'Количество файлов: {data["count"]}; '
                        f'Размер файла: {data["bs"]}; '
                        f'Средняя загрузка CPU: {current_cpu_load}\n')

    ssh_client.close()
