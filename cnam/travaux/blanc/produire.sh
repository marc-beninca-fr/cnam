#! /bin/bash

FICHIER='présentation'
DOSSIER='production'

#
rm --force --recursive "${DOSSIER}"
#
mkdir "${DOSSIER}"
#
xelatex -output-directory "${DOSSIER}" "${FICHIER}.tex"
#
xelatex -output-directory "${DOSSIER}" "${FICHIER}.tex"
#
gpg --armor --detach-sign "${DOSSIER}/${FICHIER}.pdf"
#
mv "${DOSSIER}/${FICHIER}".{pdf,pdf.asc} '.'
#
rm --force --recursive "${DOSSIER}"
#
gpg --verify "${FICHIER}.pdf.asc" 2> "${FICHIER}.pdf.vrf"
