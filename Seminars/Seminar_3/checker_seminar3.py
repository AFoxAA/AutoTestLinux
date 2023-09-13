import subprocess
import zlib
from typing import Any
import shutil


def checkout_positive(cmd: Any, text: str) -> bool:
    '''Проверка наличия строки в выводе команды'''
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    return text in result.stdout and result.returncode == 0


def checkout_negative(cmd: Any, text: str) -> bool:
    '''Проверка наличия строки в выводе команды или в выводе ошибок'''
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    return (text in result.stdout or text in result.stderr) and result.returncode != 0


def anticipated_archive_crc32_hash(cmd: Any) -> str:
    '''Получение хэш-суммы CRC32 архива из вывода команды.'''
    crc32_command_result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return crc32_command_result.stdout.strip()


def calculate_archive_crc32_hash(file_path: Any) -> str:
    '''Вычисление хэш-суммы CRC32 для содержимого архивов'''
    with open(file_path, "rb") as f:
        crc32_hash_result: int = zlib.crc32(f.read())
    return format(crc32_hash_result & 0xFFFFFFFF, '08x')


def getout(cmd):
    '''Получение хэш-суммы файла в выводе команды'''
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


def remove_test_data(test):
    '''Удаление всех тестовых данных'''
    for folder in test:
        shutil.rmtree(folder)
