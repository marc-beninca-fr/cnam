#! /bin/bash

FICHIER='présentation'
DOSSIER='production'

# purger le dossier, si nécessaire
rm --force --recursive "${DOSSIER}"
# [re]créer le dossier
mkdir "${DOSSIER}"
# 1° passe : indexer le document dans le dossier
xelatex -output-directory "${DOSSIER}" "${FICHIER}.tex"
# 2° passe : produire le document dans le dossier
xelatex -output-directory "${DOSSIER}" "${FICHIER}.tex"
# signer le document dans le dossier
gpg --armor --detach-sign "${DOSSIER}/${FICHIER}.pdf"
# extraire du dossier le document et sa signature
mv "${DOSSIER}/${FICHIER}".{pdf,pdf.asc} '.'
# [re]purger le dossier
rm --force --recursive "${DOSSIER}"
# vérifier la signature et enregistrer cette vérification
gpg --verify "${FICHIER}.pdf.asc" 2> "${FICHIER}.pdf.vrf"
