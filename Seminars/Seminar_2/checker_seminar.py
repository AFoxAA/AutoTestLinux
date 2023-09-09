import subprocess
from typing import Any


def checkout_positive(cmd: Any, text: str) -> bool:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)

    return text in result.stdout and result.returncode == 0


def checkout_negative(cmd: Any, text: str) -> bool:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)

    return (text in result.stdout or text in result.stderr) and result.returncode != 0
