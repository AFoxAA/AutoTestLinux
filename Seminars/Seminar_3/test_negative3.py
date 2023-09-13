from checker_seminar3 import (checkout_negative, anticipated_archive_crc32_hash, calculate_archive_crc32_hash)
import pytest
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_folders, make_files, create_corrupted_archive) -> None:
        '''Распаковка архива с опцией e (извлечение файлов без сохранения структуры каталогов из архива)'''
        assert checkout_negative(f'cd {data["folder_broken"]}; 7z e arx2.7z -o{data["folder_e"]} -y',
                                 'ERRORS'), 'test1 FAIL'

    def test_step2(self, make_folders, make_files, create_corrupted_archive) -> None:
        '''Распаковка архива с опцией x (извлечение файлов с сохранением структуры каталогов из архива)'''
        assert checkout_negative(f'cd {data["folder_broken"]}; 7z x arx2.7z -o{data["folder_x"]} -y',
                                 'Is not archive'), 'test2 FAIL'

    def test_step3(self, make_folders, make_files, create_corrupted_archive) -> None:
        '''Проверка содержимого архива'''
        assert checkout_negative(f'cd {data["folder_broken"]}; 7z l arx2.7z', 'Is not archive'), 'test3 FAIL'

    def test_step4(self, make_folders, make_files, create_corrupted_archive) -> None:
        '''Проверка целостности архива'''
        assert checkout_negative(f'cd {data["folder_broken"]}; 7z t arx2.7z', 'Is not archive'), 'test4 FAIL'

    def test_step5(self, make_folders, make_files, create_corrupted_archive) -> None:
        '''Проверить, что хеш одного архива не совпадает с рассчитанным другого архива(команда crc32)'''

        expected_crc32_hash: str = anticipated_archive_crc32_hash(f'crc32 {data["out"]}/arx2.7z')
        calculated_crc32_hash: str = calculate_archive_crc32_hash(f'{data["folder_broken"]}/arx2.7z')

        assert checkout_negative(f'diff -q <(echo "{expected_crc32_hash}") <(echo "{calculated_crc32_hash}")',
                                 ''), 'test5 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
