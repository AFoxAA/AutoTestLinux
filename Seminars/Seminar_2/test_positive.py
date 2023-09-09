from checker_seminar import checkout_positive
import pytest

test: str = '/home/anton/GB/task1/test'
out: str = '/home/anton/GB/task1/out'
folder_e: str = '/home/anton/GB/task1/folder_e'


def test_step1() -> None:
    # Добавление фалов в архив
    res1: bool = checkout_positive(f'cd {test}; 7z a {out}/arx2', 'Everything is Ok')
    res2: bool = checkout_positive(f'ls {out}', 'arx2.7z')
    assert res1 and res2, 'test1 FAIL'


def test_step2() -> None:
    # Распаковка архива
    res1: bool = checkout_positive(f'mkdir -p {folder_e}; 7z e {out}/arx2.7z -o{folder_e} -y', 'Everything is Ok')
    res2: bool = checkout_positive(f'ls {folder_e}', 'test1')
    res3: bool = checkout_positive(f'ls {folder_e}', 'test2')
    assert res1 and res2 and res3, 'test2 FAIL'


def test_step3() -> None:
    # проверка целостности архива
    assert checkout_positive(f'cd {out}; 7z t arx2.7z', 'Everything is Ok'), 'test3 FAIL'


def test_step4() -> None:
    # обновление содержимого архива
    assert checkout_positive(f'cd {test}; 7z u {out}/arx2.7z', 'Everything is Ok'), 'test4 FAIL'


def test_step5() -> None:
    # удаление архива
    assert checkout_positive(f'cd {out}; 7z d arx2.7z', 'Everything is Ok'), 'test5 FAIL'


def test_step6() -> None:
    # проверка содержимого архива
    assert checkout_positive(f'cd {out}; 7z l arx2.7z', '0 files'), 'test6 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
    