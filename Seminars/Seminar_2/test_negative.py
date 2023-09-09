from checker_seminar import checkout_negative
import pytest

folder_x: str = '/home/anton/GB/task1/folder_x'
folder_broken: str = '/home/anton/GB/task1/folder_broken'


def test_step1() -> None:
    # распаковка архива
    assert checkout_negative(f'cd {folder_broken}; 7z e arx2.7z -o{folder_x} -y',
                             'ERRORS'), 'test1 FAIL'


def test_step2() -> None:
    # проверка целостности архива
    assert checkout_negative(f'cd {folder_broken}; 7z t arx2.7z', 'ERRORS'), 'test2 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
    