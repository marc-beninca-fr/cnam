#! /usr/bin/python3 -B

import os
import shutil
import subprocess
import sys

ENGLISH = 'en'
FRENCH = 'fr'
LANGUAGES = [ENGLISH, FRENCH]
DOCUMENTS = [
    {ENGLISH: 'thesis', FRENCH: 'mémoire'},
    {ENGLISH: 'presentation', FRENCH: 'présentation'},
]
MAIN = 'main'
TMP = 'tmp'


def run(command):
    subprocess.call(command)


def errun(command):
    return subprocess.check_output(
        command, stderr=subprocess.STDOUT)


def build(directory, sign):
    # temporary directory
    tmp = os.path.join(directory, TMP)
    # for each language
    for language in LANGUAGES:
        # for each document
        for document in DOCUMENTS:
            # clean
            os.chdir(directory)
            wipe(tmp)
            os.makedirs(tmp)
            # move into document directory
            os.chdir(document[ENGLISH])
            # prepare variables
            variables = {'mainlanguage': language,
                         }
            # transform variables
            variables = ''.join([f'\\def\\{k}{{{v}}}'
                                 for k, v in variables.items()])
            # prepare build command
            command = ['xelatex',
                       '-output-directory', tmp,
                       f'{variables}\\input{{{MAIN}}}',
                       ]
            # if it's the main document
            if document[ENGLISH] == 'thesis':
                # pre build
                run(command)
                # build glossaries
                run(['makeglossaries', '-d', tmp, document[ENGLISH]])
                # build references
                run(['biber',
                     '--input-directory', tmp,
                     '--output-directory', tmp,
                     MAIN,
                     ])
                # re build
                run(command)
            # final build
            run(command)
            # rename the document
            pdf = f'{document[language]}.pdf'
            os.rename(os.path.join(tmp, f'{MAIN}.pdf'),
                      os.path.join(tmp, pdf),
                      )
            # if signature is disabled
            if not sign:
                # fetch the document from temporary directory
                os.rename(os.path.join(tmp, pdf),
                          os.path.join(directory, pdf),
                          )
            # if signature is enabled
            else:
                # sign the document
                run(['gpg',
                     '--armor',
                     '--detach-sign',
                     os.path.join(tmp, pdf),
                     ])
                signature = f'{pdf}.asc'
                # fetch the document and signature from temporary directory
                for f in [pdf, signature]:
                    os.rename(os.path.join(tmp, f),
                              os.path.join(directory, f),
                              )
                # verify the document signature
                lines = errun(['gpg', '--verify',
                               os.path.join(directory, signature),
                               os.path.join(directory, pdf),
                               ]).decode('u8').splitlines()
                id = lines[2].index('"')
                lines = [
                    lines[0],
                    lines[1],
                    lines[2][:id] + lines[4][id:]
                    .replace('@', ' @ ')
                    .replace('.', ' ⋅ ')
                ] + lines[5:]
                # write verification file
                buffer = os.linesep.join(lines).encode('u8')
                with open(os.path.join(directory, f'{pdf}.vrf'), 'bw') as f:
                    f.write(buffer)
    # clean
    wipe(tmp)


def wipe(directory):
    shutil.rmtree(directory, ignore_errors=True)


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    build(directory, len(sys.argv) == 1)


if __name__ == '__main__':
    main()
