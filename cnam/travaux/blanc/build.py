#! /usr/bin/python3 -B

import os
import subprocess

DOCUMENTS = [
    'document',
    'présentation',
]


def build():
    for document in DOCUMENTS:
        command = ['xelatex', f'{document}.tex']
        for _ in range(2):
            subprocess.call(command)


def clean():
    _, _, files = next(os.walk(directory))
    for file in files:
        name, ext = os.path.splitext(file)
        if ext in ['.aux', '.log']:
            os.remove(file)


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    os.chdir(directory)
    build()
    clean()


if __name__ == '__main__':
    main()
