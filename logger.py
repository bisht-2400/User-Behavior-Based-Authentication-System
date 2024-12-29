import os
from datetime import datetime


def make_log_file() -> None:
    if not os.path.exists("logs/log_file.txt"):
        with open("logs/log_file.txt", 'w') as file:
            file.write(get_time() + " Log File created")


def get_time() -> str:
    now = datetime.now()
    return now.strftime("(%m/%d/%Y)%H:%M:%S:: ")


class Logger:
    def __init__(self):
        make_log_file()
        self.file_name = "logs/log_file.txt"

    def write_log(self, msg) -> None:
        with open(self.file_name, 'a+') as file:
            file.write('\n' + get_time() + msg)
