#! /usr/bin/python3 -B

import os
import shutil
import subprocess

import sphinx.cmd.build

TRAVAUX = ['thesis']
INPUT = ['cnam']
OUTPUT = 'out'


def others():
    travaux = os.path.join('cnam', 'travaux')
    for travail in TRAVAUX:
        subprocess.call([os.path.join(travaux, travail, 'build.py')])


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    os.chdir(directory)
    others()
    output_directory = os.path.join(directory, OUTPUT)
    shutil.rmtree(output_directory, ignore_errors=True)
    for doc in INPUT:
        arguments = [
            '-E',
            '-j', '2',
            '-b', 'html',
            '-D', 'project={}'.format(doc),
            '-D', 'master_doc={}'.format('index'),
            '-D', 'html_theme={}'.format('sphinx_rtd_theme'),
            # '-C',
            '-c', directory,
            os.path.join(directory, doc),
            os.path.join(output_directory, doc),
        ]
        sphinx.cmd.build.build_main(arguments)


if __name__ == '__main__':
    main()
