from checker_homework import checkout_negative, anticipated_archive_crc32_hash, calculate_archive_crc32_hash
import pytest

out: str = '/home/anton/GB/task1/out'
folder_e: str = '/home/anton/GB/task1/folder_e'
folder_x: str = '/home/anton/GB/task1/folder_x'
folder_broken: str = '/home/anton/GB/task1/folder_broken'


def test_step1() -> None:
    '''Распаковка архива с опцией e (извлечение файлов без сохранения структуры каталогов из архива)'''
    assert checkout_negative(f'cd {folder_broken}; 7z e arx2.7z -o{folder_e} -y',
                             'ERRORS'), 'test1 FAIL'


def test_step2() -> None:
    '''Распаковка архива с опцией x (извлечение файлов с сохранением структуры каталогов из архива)'''
    assert checkout_negative(f'cd {folder_broken}; 7z x arx2.7z -o{folder_x} -y',
                             'ERRORS'), 'test2 FAIL'


def test_step3() -> None:
    '''Проверка содержимого архива'''
    assert checkout_negative(f'cd {folder_broken}; 7z l arx2.7z', 'Is not archive'), 'test3 FAIL'


def test_step4() -> None:
    '''Проверка целостности архива'''
    assert checkout_negative(f'cd {folder_broken}; 7z t arx2.7z', 'ERRORS'), 'test4 FAIL'


def test_step5() -> None:
    '''Проверить, что хеш одного архива не совпадает с рассчитанным другого архива(команда crc32)'''
    expected_crc32_hash: str = anticipated_archive_crc32_hash(f'crc32 {out}/arx2.7z')
    calculated_crc32_hash: str = calculate_archive_crc32_hash(f'{folder_broken}/arx2.7z')

    assert calculated_crc32_hash != expected_crc32_hash, f'test7 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
    