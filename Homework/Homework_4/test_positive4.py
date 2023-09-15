import pytest
import yaml
from typing import Any
from sshcheckers import (ssh_checkout, anticipated_archive_crc32_hash, calculate_archive_crc32_hash, getout,
                         remove_test_data, upload_files, save_log)

with open('config.yaml') as f:
    data: Any = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, make_files, start_time) -> None:
        '''Добавление фалов в архив'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'ls {data["out"]}', f'arx2.{data["archive_type"]}', True))

        assert all(result), 'test1 FAIL'

    def test_step2(self, make_folders, make_files, start_time) -> None:
        '''Проверка содержимого архива'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["out"]}; 7z l arx2.{data["archive_type"]}', '5 files', True))

        assert all(result), 'test2 FAIL'

    def test_step3(self, make_folders, make_files, start_time) -> None:
        '''Распаковка архива с опцией e (извлечение файлов без сохранения структуры каталогов из архива)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["out"]}; 7z e arx2.{data["archive_type"]} -o{data["folder_e"]} -y',
                                   'Everything is Ok', True))

        for item in make_files:
            result.append(ssh_checkout(data['ip'], data['user'], data['passwd'], f'ls {data["folder_e"]}', item))
        assert all(result), 'test3 FAIL'

    def test_step4(self, make_folders, make_files, make_subfolder, start_time) -> None:
        '''Распаковка архива с опцией x (извлечение файлов с сохранением структуры каталогов из архива)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["out"]}; 7z x arx2.{data["archive_type"]} -o{data["folder_x"]} -y',
                                   'Everything is Ok', True))

        for item in make_files:
            result.append(ssh_checkout(data['ip'], data['user'], data['passwd'], f'ls {data["folder_x"]}', item))

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'ls {data["folder_x"]}', make_subfolder[0], True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'ls {data["folder_x"]}/{make_subfolder[0]}', make_subfolder[1], True))
        assert all(result), "test4 FAIL"

    def test_step5(self, make_folders, make_files, start_time) -> None:
        '''Проверка целостности архива'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["out"]}; 7z t arx2.{data["archive_type"]}', 'Everything is Ok', True))

        assert all(result), 'test5 FAIL'

    def test_step6(self, make_folders, make_files, start_time) -> None:
        '''Обновление содержимого архива'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z u {data["out"]}/arx2.{data["archive_type"]}',
                                   'Everything is Ok', True))

        assert all(result), 'test6 FAIL'

    def test_step7(self, make_folders, make_files, start_time) -> None:
        '''Проверить, что хеш архива совпадает с рассчитанным (команда crc32)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        expected_crc32_hash: str = anticipated_archive_crc32_hash(data['ip'], data['user'], data['passwd'],
                                                                  f'crc32 {data["out"]}/arx2.{data["archive_type"]}')
        calculated_crc32_hash: str = calculate_archive_crc32_hash(data['ip'], data['user'], data['passwd'],
                                                                  f'{data["out"]}/arx2.{data["archive_type"]}')
        result.append(calculated_crc32_hash == expected_crc32_hash)

        assert all(result), f'test7 FAIL'

    def test_step8(self, make_folders, make_files, start_time):
        '''Проверить, что хеш файла совпадает с рассчитанным (команда crc32)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))

        for item in make_files:
            result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                       f'cd {data["test"]}; 7z h {item}', 'Everything is Ok', True))
            hash: str = getout(data['ip'], data['user'], data['passwd'], f'cd {data["test"]}; crc32 {item}').upper()
            result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                       f'cd {data["test"]}; 7z h {item}', hash, True))

        assert all(result), "test8 FAIL"

    def test_step9(self, start_time) -> None:
        '''Установка пакета на удаленной машине'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []

        upload_files(data["ip"], data["user"], data["passwd"], f'{data["pkgname"]}.{data["file_extension"]}',
                     f'{data["test"]}{data["pkgname"]}.{data["file_extension"]}')

        result.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f'echo {data["passwd"]} | sudo -S dpkg -i {data["test"]}{data["pkgname"]}.{data["file_extension"]}',
                                "Настраивается пакет", True))

        result.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f'echo {data["passwd"]} | sudo -S dpkg -s {data["pkgname"]}',
                                "Status: install ok installed", True))

        assert all(result), "test9 FAIL"

    def test_step10(self, make_folders, make_files, start_time) -> None:
        '''Очистка архива'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        result: list[bool] = []
        test_data: list = [data['test'], data['out'], data['folder_e'], data['folder_x'], data['folder_broken']]

        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["test"]}; 7z a {data["out"]}/arx2 -t{data["archive_type"]}',
                                   'Everything is Ok', True))
        result.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                   f'cd {data["out"]}; 7z d arx2.{data["archive_type"]}', 'Everything is Ok', True))

        remove_test_data(data['ip'], data['user'], data['passwd'], test_data)

        assert all(result), 'test10 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
