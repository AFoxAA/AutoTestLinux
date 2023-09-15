import pytest
import yaml
from typing import Any
from sshcheckers import (ssh_checkout, anticipated_archive_crc32_hash, calculate_archive_crc32_hash, remove_test_data,
                         save_log)

with open('config.yaml') as f:
    data: Any = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_folders, make_files, create_corrupted_archive, start_time) -> None:
        '''Распаковка архива с опцией e (извлечение файлов без сохранения структуры каталогов из архива)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_broken"]}; 7z e arx2.{data["archive_type"]} -o{data["folder_e"]} -y',
                            'Is not archive', False), 'test1 FAIL'

    def test_step2(self, make_folders, make_files, create_corrupted_archive, start_time) -> None:
        '''Распаковка архива с опцией x (извлечение файлов с сохранением структуры каталогов из архива)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_broken"]}; 7z x arx2.{data["archive_type"]} -o{data["folder_x"]} -y',
                            'Is not archive', False), 'test2 FAIL'

    def test_step3(self, make_folders, make_files, create_corrupted_archive, start_time) -> None:
        '''Проверка содержимого архива'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_broken"]}; 7z l arx2.{data["archive_type"]}',
                            'Is not archive', False), 'test3 FAIL'

    def test_step4(self, make_folders, make_files, create_corrupted_archive, start_time) -> None:
        '''Проверка целостности архива'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_broken"]}; 7z t arx2.{data["archive_type"]}',
                            'Is not archive', False), 'test4 FAIL'

    def test_step5(self, make_folders, make_files, create_corrupted_archive, start_time) -> None:
        '''Проверить, что хеш одного архива не совпадает с рассчитанным другого архива(команда crc32)'''
        save_log(data['ip'], data['user'], data['passwd'], start_time, data["stat_file"])
        test_data: list = [data['test'], data['out'], data['folder_e'], data['folder_x'], data['folder_broken']]

        expected_crc32_hash: str = anticipated_archive_crc32_hash(data['ip'], data['user'], data['passwd'],
                                                                  f'crc32 {data["out"]}/arx2.{data["archive_type"]}')
        calc_crc32_hash: str = calculate_archive_crc32_hash(data['ip'], data['user'], data['passwd'],
                                                            f'{data["folder_broken"]}/arx2.{data["archive_type"]}')

        remove_test_data(data['ip'], data['user'], data['passwd'], test_data)

        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'diff -q <(echo "{expected_crc32_hash}") <(echo "{calc_crc32_hash}")',
                            '', False), 'test5 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
