from checker_homework import checkout_positive, anticipated_archive_crc32_hash, calculate_archive_crc32_hash
import pytest

test: str = '/home/anton/GB/task1/test'
out: str = '/home/anton/GB/task1/out'
folder_e: str = '/home/anton/GB/task1/folder_e'
folder_x: str = '/home/anton/GB/task1/folder_x'


def test_step1() -> None:
    '''Добавление фалов в архив'''
    result: list[bool] = []

    result.append(checkout_positive(f'cd {test}; 7z a {out}/arx2', 'Everything is Ok'))
    result.append(checkout_positive(f'ls {out}', 'arx2.7z'))

    assert all(result), 'test1 FAIL'


def test_step2() -> None:
    '''Проверка содержимого архива'''
    result: list[bool] = []

    result.append(checkout_positive(f'cd {out}; 7z l arx2.7z', '2 folders'))
    result.append(checkout_positive(f'cd {out}; 7z l arx2.7z', '3 files'))

    assert all(result), 'test2 FAIL'


def test_step3() -> None:
    '''Распаковка архива с опцией e (извлечение файлов без сохранения структуры каталогов из архива)'''
    result: list[bool] = []

    result.append(checkout_positive(f'mkdir -p {folder_e}; 7z e {out}/arx2.7z -o{folder_e} -y', 'Everything is Ok'))
    result.append(checkout_positive(f'ls {folder_e}', 'folder_1'))
    result.append(checkout_positive(f'ls {folder_e}', 'folder_2'))
    result.append(checkout_positive(f'ls {folder_e}', 'test1.txt'))
    result.append(checkout_positive(f'ls {folder_e}', 'test2.txt'))
    result.append(checkout_positive(f'ls {folder_e}', 'test3.txt'))

    assert all(result), 'test3 FAIL'


def test_step4() -> None:
    '''Распаковка архива с опцией x (извлечение файлов с сохранением структуры каталогов из архива)'''
    result: list[bool] = []

    result.append(checkout_positive(f'mkdir -p {folder_x}; 7z x {out}/arx2.7z -o{folder_x} -y', 'Everything is Ok'))
    result.append(checkout_positive(f'ls {folder_x}', 'folder_1'))
    result.append(checkout_positive(f'ls {folder_x}', 'folder_2'))
    result.append(checkout_positive(f'ls {folder_x}/folder_1', 'test1.txt'))
    result.append(checkout_positive(f'ls {folder_x}/folder_2', 'test2.txt'))
    result.append(checkout_positive(f'ls {folder_x}', 'test3.txt'))

    assert all(result), 'test4 FAIL'


def test_step5() -> None:
    '''Проверка целостности архива'''
    assert checkout_positive(f'cd {out}; 7z t arx2.7z', 'Everything is Ok'), 'test5 FAIL'


def test_step6() -> None:
    '''Обновление содержимого архива'''
    assert checkout_positive(f'cd {test}; 7z u {out}/arx2.7z', 'Everything is Ok'), 'test6 FAIL'


def test_step7() -> None:
    '''Проверить, что хеш совпадает с рассчитанным (команда crc32)'''
    expected_crc32_hash: str = anticipated_archive_crc32_hash(f'crc32 {out}/arx2.7z')
    calculated_crc32_hash: str = calculate_archive_crc32_hash(f'{out}/arx2.7z')

    assert calculated_crc32_hash == expected_crc32_hash, f'test7 FAIL'


def test_step8() -> None:
    '''Удаление архива'''
    assert checkout_positive(f'cd {out}; 7z d arx2.7z', 'Everything is Ok'), 'test8 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
    