import pytest
from checker_homework3 import checkout_positive
import random
import string
import yaml
from datetime import datetime
from typing import Any, Generator

with open('config.yaml') as f:
    data: Any = yaml.safe_load(f)


@pytest.fixture()
def make_folders() -> bool:
    '''Создание директорий'''
    return checkout_positive(f'mkdir {data["test"]} {data["folder_e"]} {data["folder_x"]} {data["folder_broken"]}', '')


@pytest.fixture(autouse=True)
def clear_folders() -> None:
    '''Удаление директорий'''
    checkout_positive(
        f'rm -rf {data["test"]} {data["out"]} {data["folder_e"]} {data["folder_x"]} {data["folder_broken"]}', '')


@pytest.fixture()
def make_files() -> list[str]:
    '''Создание файлов'''
    list_of_files: list[str] = []

    for i in range(data["count"]):
        filename: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.txt'
        if checkout_positive(f'cd {data["test"]}; dd if=/dev/urandom of={filename} bs={data["bs"]} '
                             f'count={data["count"]} iflag=fullblock', ''):
            list_of_files.append(filename)

    return list_of_files


@pytest.fixture()
def make_subfolder() -> tuple:
    '''Создание поддиректорий с файлами'''
    testfilename: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.txt'
    subfoldername: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    if not checkout_positive(f'cd {data["test"]}; mkdir {subfoldername}', ''):
        return None, None
    if not checkout_positive(f'cd {data["test"]}/{subfoldername}; dd if=/dev/urandom of={testfilename} '
                             f'bs={data["bs"]} count={data["count"]} iflag=fullblock', ''):
        return subfoldername, None

    return subfoldername, testfilename


@pytest.fixture()
def create_corrupted_archive() -> None:
    '''Создание битого архива'''
    checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}', 'Everything is Ok')
    checkout_positive(f'cp {data["out"]}/arx2.{data["archive_type"]} {data["folder_broken"]}', '')
    checkout_positive(f'truncate -s 1 {data["folder_broken"]}/arx2.{data["archive_type"]}', '')


@pytest.fixture(autouse=True)
def print_time() -> Generator[Any, Any, None]:
    '''Вывод времени начала и окончания выполнения теста'''
    print(f"Начало: {datetime.now().strftime('%H:%M:%S.%f')}")
    yield
    print(f"Окончание: {datetime.now().strftime('%H:%M:%S.%f')}")


@pytest.fixture()
def collect_statistics_for_test(request) -> None:
    '''Создание файла со статистикой, с внесением информации в этот файл'''
    test_start_time: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_cpu_load: str = open('/proc/loadavg').read().strip()
    test_name: Any = request.node.name
    class_name: str = request.cls.__name__ if request.cls else ""

    with open('test_statistics.txt', 'a', encoding='utf-8') as stat_file:
        stat_file.write(f'Время запуска: {test_start_time}; '
                        f'Название класса:{class_name}; '
                        f'Название теста: {test_name}; '
                        f'Количество файлов: {data["count"]}; '
                        f'Размер файла: {data["bs"]}; '
                        f'Средняя загрузка: {current_cpu_load}\n')
