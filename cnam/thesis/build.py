#! /usr/bin/python3 -B

import os
import shutil
import subprocess
import sys

MAIN = 'main'
TMP = 'tmp'

ENGLISH = 'english'
FRENCH = 'french'
LANGUAGES = [ENGLISH, FRENCH]

DOCUMENTS = [
    {ENGLISH: 'thesis', FRENCH: 'mémoire'},
    # {ENGLISH: 'presentation', FRENCH: 'présentation'},
]


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
        # languages
        other_languages = [lang for lang in LANGUAGES if lang is not language]
        languages = [language, *other_languages]
        other_languages = ','.join(other_languages)
        summaries = ''.join(
            [f'\\summary{{{lang}}}' for lang in languages])
        # display languages
        for item in ['', language, other_languages, languages, summaries]:
            print(item)
        # for each document
        for document in DOCUMENTS:
            # display language
            print()
            print(document[language])
            # clean
            os.chdir(directory)
            wipe(tmp)
            os.makedirs(tmp)
            # move into document directory
            os.chdir(document[ENGLISH])
            # prepare variables
            variables = {
                'name': MAIN,
                'ENGLISH': ENGLISH,
                'FRENCH': FRENCH,
                'mainlanguage': language,
                'otherlanguages': other_languages,
                'summaries': summaries,
            }
            # transform variables
            variables = ''.join([f'\\def\\{k}{{{v}}}'
                                 for k, v in variables.items()])
            # prepare build command
            command = ['xelatex',
                       '-output-directory', tmp,
                       f'{variables}\\input{{{MAIN}}}',
                       ]
            # pre build
            run(command)
            # if it's the main document
            if document[ENGLISH] == 'thesis':
                # build glossaries
                run(['makeglossaries',
                     '-d', tmp,
                     MAIN,
                     ])
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
