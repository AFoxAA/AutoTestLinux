import subprocess
import re
from typing import List


def text_checking_in_command_output(command: List[str], text: str, split_text: bool = False) -> bool:
    result_command_output: str = (
        subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True, encoding='utf-8')).stdout

    if split_text:
        words_list: List[str] = re.findall(r'\b\w+\b', result_command_output)
        result_command_output: str = ' '.join(words_list)

    return text in result_command_output


if __name__ == '__main__':
    command_list: List[str] = ['cat /etc/os-release']
    text_search: str = 'VERSION 23 04 Lunar Lobster'
    text_was_found: bool = text_checking_in_command_output(command_list, text_search, split_text=True)
    print(f'\nРезультат:\n{text_search}: {text_was_found}')
