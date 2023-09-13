from checker_seminar3 import (checkout_positive, anticipated_archive_crc32_hash, calculate_archive_crc32_hash,
                              remove_test_data, getout)
import pytest
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, make_files) -> None:
        '''Добавление фалов в архив'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'ls {data["out"]}', 'arx2.7z'))

        assert all(result), 'test1 FAIL'

    def test_step2(self, make_folders, make_files) -> None:
        '''Проверка содержимого архива'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'cd {data["out"]}; 7z l arx2.7z', '5 files'))

        assert all(result), 'test2 FAIL'

    def test_step3(self, make_folders, make_files) -> None:
        '''Распаковка архива с опцией e (извлечение файлов без сохранения структуры каталогов из архива)'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'cd {data["out"]}; 7z e arx2.7z -o{data["folder_e"]} -y', 'Everything is Ok'))

        for item in make_files:
            result.append(checkout_positive(f'ls {data["folder_e"]}', item))
        assert all(result), 'test3 FAIL'

    def test_step4(self, make_folders, make_files, make_subfolder) -> None:
        '''Распаковка архива с опцией x (извлечение файлов с сохранением структуры каталогов из архива)'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'cd {data["out"]}; 7z x arx2.7z -o{data["folder_x"]} -y', 'Everything is Ok'))

        for item in make_files:
            result.append(checkout_positive(f'ls {data["folder_x"]}', item))

        result.append(checkout_positive(f'ls {data["folder_x"]}', make_subfolder[0]))
        result.append(checkout_positive(f'ls {data["folder_x"]}/{make_subfolder[0]}', make_subfolder[1]))
        assert all(result), "test4 FAIL"

    def test_step5(self, make_folders, make_files) -> None:
        '''Проверка целостности архива'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'cd {data["out"]}; 7z t arx2.7z', 'Everything is Ok'))

        assert all(result), 'test5 FAIL'

    def test_step6(self, make_folders, make_files) -> None:
        '''Обновление содержимого архива'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'cd {data["test"]}; 7z u {data["out"]}/arx2.7z', 'Everything is Ok'))

        assert all(result), 'test6 FAIL'

    def test_step7(self, make_folders, make_files) -> None:
        '''Проверить, что хеш архива совпадает с рассчитанным (команда crc32)'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        expected_crc32_hash: str = anticipated_archive_crc32_hash(f'crc32 {data["out"]}/arx2.7z')
        calculated_crc32_hash: str = calculate_archive_crc32_hash(f'{data["out"]}/arx2.7z')
        result.append(calculated_crc32_hash == expected_crc32_hash)

        assert all(result), f'test7 FAIL'

    def test_step8(self, make_folders, make_files):
        '''Проверить, что хеш файла совпадает с рассчитанным (команда crc32)'''
        result: list[bool] = []

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))

        for item in make_files:
            result.append(checkout_positive(f'cd {data["test"]}; 7z h {item}', "Everything is Ok"))
            hash = getout(f'cd {data["test"]}; crc32 {item}').upper()
            result.append(checkout_positive(f'cd {data["test"]}; 7z h {item}', hash))

        assert all(result), "test8 FAIL"

    def test_step9(self, make_folders, make_files) -> None:
        '''Удаление архива'''
        result: list[bool] = []
        test_data = [data["test"], data["out"], data["folder_e"], data["folder_x"]]

        result.append(checkout_positive(f'cd {data["test"]}; 7z a {data["out"]}/arx2', 'Everything is Ok'))
        result.append(checkout_positive(f'cd {data["out"]}; 7z d arx2.7z', 'Everything is Ok'))

        remove_test_data(test_data)

        assert all(result), 'test9 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
