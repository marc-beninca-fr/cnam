#! /usr/bin/python3 -B

import os
import shutil
import subprocess
import sys

AUTHOR = 'Marc BENINCA'
MAIN = 'main'
TMP = 'tmp'

ENGLISH = 'en'
FRENCH = 'fr'
LANGUAGES = [ENGLISH, FRENCH]

DOCUMENTS = [
    {ENGLISH: 'thesis', FRENCH: 'mémoire'},
    {ENGLISH: 'presentation', FRENCH: 'présentation'},
]
TITLE_LONG = {
    ENGLISH: 'Incremental Live Operating Systems',
    FRENCH: 'Systèmes d’exploitation autonomes incrémentaux',
}
SUBTITLE = {
    ENGLISH: 'a reversal of conventional approaches',
    FRENCH: 'une inversion des approches conventionnelles',
}
DATE_SHORT = '2021'
DATE_LONG = {
    ENGLISH: f'Month DD, {DATE_SHORT}',
    FRENCH: f'JJ Mois {DATE_SHORT}',
}
TYPE_SHORT = {
    ENGLISH: 'Thesis',
    FRENCH: 'Mémoire',
}
TYPE_LONG = {
    ENGLISH: f'CNAM Master\'s {TYPE_SHORT[ENGLISH]}',
    FRENCH: f'{TYPE_SHORT[FRENCH]} d’Ingénieur CNAM',
}


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
            [f'\\input{{summary.{lang}}}' for lang in languages])
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
                'author': AUTHOR,
                'titlelong': TITLE_LONG[language],
                'titlesub': SUBTITLE[language],
                'dateshort': DATE_SHORT,
                'datelong': DATE_LONG[language],
                'typeshort': TYPE_SHORT[language],
                'typelong': TYPE_LONG[language],
                'name': MAIN,
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
            # if it's the main document
            if document[ENGLISH] == 'thesis':
                # pre build
                run(command)
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
