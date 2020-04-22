#! /usr/bin/python3 -B

import os
import subprocess

DOCUMENTS = [
    'document',
    'présentation',
]


def build(directory):
    os.chdir(directory)
    for document in DOCUMENTS:
        command = ['xelatex', f'{document}.tex']
        for _ in range(2):
            subprocess.call(command)


def clean(directory):
    os.chdir(directory)
    _, _, files = next(os.walk(directory))
    for file in files:
        name, ext = os.path.splitext(file)
        if ext in ['.aux', '.log', '.toc']:
            os.remove(file)


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    build(directory)
    clean(directory)


if __name__ == '__main__':
    main()
