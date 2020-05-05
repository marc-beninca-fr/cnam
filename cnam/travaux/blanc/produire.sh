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
gpg --armor --detach-sign "${TEMPORAIRE}/${NOM}.pdf"
#
mv "${TEMPORAIRE}/${NOM}.pdf" "${TEMPORAIRE}/${NOM}.pdf.asc" '.'
#
rm --force --recursive "${TEMPORAIRE}"
#
gpg --verify "${NOM}.pdf.asc" "${NOM}.pdf" 2> "${NOM}.pdf.vrf"
