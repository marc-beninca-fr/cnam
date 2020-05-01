#! /usr/bin/python3 -B

import os
import shutil
import subprocess

DOCUMENTS = [
    ('document', 'mémoire'),
    ('presentation', 'présentation'),
]
TMP = 'tmp'


def run(command):
    subprocess.call(command)


def errun(command):
    return subprocess.check_output(
        command, stderr=subprocess.STDOUT)


def build():
    for en, fr in DOCUMENTS:
        command = ['xelatex',
            '-output-directory', TMP,
            en,
        ]
        run(command)
        run(['makeglossaries',
            '-d', TMP,
            en,
        ])
        run(['biber',
            '--input-directory', TMP,
            '--output-directory', TMP,
            en,
        ])
        run(command)
        run(command)
        os.rename(os.path.join(TMP, f'{en}.pdf'),
            os.path.join(TMP, f'{fr}.pdf'))
        pdf = f'{fr}.pdf'
        run(['gpg',
            '--armor',
            '--detach-sign',
            os.path.join(TMP, pdf),
        ])
        signature = f'{pdf}.asc'
        for f in [pdf, signature]:
            os.rename(os.path.join(TMP, f), f)
        lines = errun(['gpg',
            '--verify', signature, pdf,
        ]).decode('u8').splitlines()
        using = lines[1].index('using')
        id = lines[2].index('"')
        lines = [
            lines[0][:using] + lines[1][using:],
            lines[2][:id] + lines[4][id:]
            .replace('@', ' @ ')
            .replace('.', ' ⋅ ')
        ] + lines[5:]
        buffer = os.linesep.join(lines).encode('u8')
        with open(f'{pdf}.vrf', 'bw') as f:
            f.write(buffer)


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
