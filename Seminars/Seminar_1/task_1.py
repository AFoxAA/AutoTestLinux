import subprocess
from typing import List


def verify_ubuntu_version():
    result = subprocess.run('cat /etc/os-release', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    os_info: str = result.stdout

    if result.returncode == 0:
        os_release_lines: List[str] = os_info.split('\n')
        verification_status: str = 'SUCCESS' if ('PRETTY_NAME="Ubuntu 23.04"' in os_release_lines and
                                                 'VERSION="23.04 (Lunar Lobster)"' in os_release_lines) else 'FAIL'
        return verification_status
    else:
        return 'FAIL: CODE != 0'


if __name__ == '__main__':
    print(f'\nПолученный результат: {verify_ubuntu_version()}')
