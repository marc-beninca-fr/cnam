#! /usr/bin/python3 -B

import os
import shutil
import subprocess

DOCUMENTS = [
    'document',
    'présentation',
]
TMP = 'tmp'


def run(args):
    subprocess.call(args)


def build():
    for document in DOCUMENTS:
        command = ['xelatex',
            '-output-directory', TMP,
            document,
        ]
        run(command)
        run(['makeglossaries',
            '-d', TMP,
            document,
        ])
        run(['biber',
            '--input-directory', TMP,
            '--output-directory', TMP,
            document,
        ])
        run(command)
        run(command)
        pdf = f'{document}.pdf'
        os.rename(os.path.join(TMP, pdf), pdf)
        run(['gpg',
            '--armor',
            '--clear-sign', pdf,
        ])


def clean():
    shutil.rmtree(TMP, ignore_errors=True)


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    os.chdir(directory)
    clean()
    os.makedirs(TMP)
    build()
    clean()


if __name__ == '__main__':
    main()
