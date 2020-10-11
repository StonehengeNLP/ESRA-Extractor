import sys
import subprocess


def _extract():
    list_files = subprocess.run(["python", "./spert/spert.py", "--config", "configs/extract.conf"])
    print(list_files)

if __name__ == '__main__':
    _extract()