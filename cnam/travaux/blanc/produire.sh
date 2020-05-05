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
mv "${DOSSIER}/${FICHIER}.pdf" "${DOSSIER}/${FICHIER}.pdf.asc" '.'
#
rm --force --recursive "${DOSSIER}"
#
gpg --verify "${FICHIER}.pdf.asc" "${FICHIER}.pdf" 2> "${FICHIER}.pdf.vrf"
