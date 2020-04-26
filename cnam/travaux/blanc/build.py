#! /usr/bin/python3 -B

import os
import subprocess

DOCUMENTS = [
    'document',
    'présentation',
]
PURGE = [
    '.aux', '.log', '.toc',
    '.acn', '.acr', '.alg',
    '.glg', '.glo', '.gls',
    '.glsdefs', '.ist',
]


def run(*args):
    subprocess.call(args)


def build(directory):
    os.chdir(directory)
    for document in DOCUMENTS:
        run('xelatex', f'{document}.tex')
        run('makeglossaries', f'{document}')
        run('xelatex', f'{document}.tex')


def clean(directory):
    os.chdir(directory)
    _, _, files = next(os.walk(directory))
    for file in files:
        name, ext = os.path.splitext(file)
        if ext in PURGE:
            os.remove(file)


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    clean(directory)
    build(directory)
    clean(directory)


if __name__ == '__main__':
    main()
