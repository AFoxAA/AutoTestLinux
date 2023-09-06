import subprocess
from typing import List


def text_checking_in_command_output(command: List[str], text: str) -> bool:
    result_command_output: str = (
        subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True, encoding='utf-8')).stdout

    return text in result_command_output


if __name__ == '__main__':
    command_list: List[str] = ['cat /etc/os-release']
    text_search: str = '23.04 (Lunar Lobster)'
    text_was_found: bool = text_checking_in_command_output(command_list, text_search)
    print(f'\nПолученный результат:\n{text_search}: {text_was_found}')
