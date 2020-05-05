#! /bin/bash

NOM='presentation'
TEMPORAIRE='tmp'

function produire {
xelatex -output-directory "${TEMPORAIRE}" "${NOM}.tex" }

function purger {
rm --force --recursive "${TEMPORAIRE}" }

purger
produire
produire
mv "${TEMPORAIRE}/${NOM}.pdf" '.'
purger
gpg --armor --detach-sign "${NOM}.pdf"
gpg --verify "${NOM}.pdf.asc"
