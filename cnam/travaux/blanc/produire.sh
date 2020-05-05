#! /bin/bash

NOM='presentation'
TEMPORAIRE='tmp'

#
rm --force --recursive "${TEMPORAIRE}"
#
mkdir "${TEMPORAIRE}"
#
xelatex -output-directory "${TEMPORAIRE}" "${NOM}.tex"
#
xelatex -output-directory "${TEMPORAIRE}" "${NOM}.tex"
#
mv "${TEMPORAIRE}/${NOM}.pdf" '.'
#
rm --force --recursive "${TEMPORAIRE}"
#
gpg --armor --detach-sign "${NOM}.pdf"
#
gpg --verify "${NOM}.pdf.asc"
