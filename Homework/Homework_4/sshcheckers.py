import paramiko
from paramiko import SSHClient, SFTPClient, Transport
from typing import Any
import zlib


def ssh_checkout(host, user, passwd, cmd, text, check_exit_code=True, port=22) -> bool:
    '''Проверка наличия строки в выводе команды или в выводе ошибок'''
    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=passwd, port=port)

    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    exit_code: Any = stdout.channel.recv_exit_status()
    output: Any = (stdout.read() + stderr.read()).decode("utf-8")

    ssh_client.close()

    if check_exit_code:
        return text in output and exit_code == 0
    return text in output and exit_code != 0


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"\nЗагружаем файл {local_path} в каталог {remote_path}")
    transport: Transport = paramiko.Transport(host, port)
    transport.connect(None, username=user, password=passwd)
    sftp: SFTPClient = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def anticipated_archive_crc32_hash(host, user, passwd, cmd, port=22) -> Any:
    '''Получение хэш-суммы CRC32 архива из вывода команды на удаленном сервере.'''
    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=passwd, port=port)

    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    crc32_command_result: Any = (stdout.read() + stderr.read()).decode("utf-8")

    ssh_client.close()

    return crc32_command_result.strip()


def calculate_archive_crc32_hash(host, user, passwd, file_path, port=22) -> str:
    '''Вычисление хэш-суммы CRC32 для содержимого архивов'''
    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=passwd, port=port)

    sftp: Any = ssh_client.open_sftp()

    with sftp.open(file_path) as remote_file:
        crc32_hash_result: int = zlib.crc32(remote_file.read())

    ssh_client.close()

    return format(crc32_hash_result & 0xFFFFFFFF, '08x')


def getout(host, user, passwd, cmd, port=22) -> str:
    '''Получение хэш-суммы файла в выводе команды'''
    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=passwd, port=port)

    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    output: Any = (stdout.read() + stderr.read()).decode("utf-8")

    ssh_client.close()

    return output


def remove_test_data(host, user, passwd, folders_to_remove, port=22) -> None:
    '''Удаление всех тестовых данных'''
    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=passwd, port=port)

    for folder in folders_to_remove:
        cmd: str = f"rm -rf {folder}"
        ssh_client.exec_command(cmd)

    ssh_client.close()


def save_log(host, user, passwd, starttime, name, port=22) -> None:
    ssh_client: SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(host, username=user, password=passwd, port=port)
    cmd: str = f'journalctl --since "{starttime}"'
    stdin, stdout, stderr = ssh_client.exec_command(cmd)

    result: Any = (stdout.read() + stderr.read()).decode("utf-8")

    with open(name, 'w', encoding='utf-8') as f:
        f.write(result)

    ssh_client.close()
