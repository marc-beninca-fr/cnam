#! /bin/bash

FICHIER='présentation'
TEMPORAIRE='tmp'

#
rm --force --recursive "${TEMPORAIRE}"
#
mkdir "${TEMPORAIRE}"
#
xelatex -output-directory "${TEMPORAIRE}" "${FICHIER}.tex"
#
xelatex -output-directory "${TEMPORAIRE}" "${FICHIER}.tex"
#
gpg --armor --detach-sign "${TEMPORAIRE}/${FICHIER}.pdf"
#
mv "${TEMPORAIRE}/${FICHIER}.pdf" "${TEMPORAIRE}/${FICHIER}.pdf.asc" '.'
#
rm --force --recursive "${TEMPORAIRE}"
#
gpg --verify "${FICHIER}.pdf.asc" "${FICHIER}.pdf" 2> "${FICHIER}.pdf.vrf"
