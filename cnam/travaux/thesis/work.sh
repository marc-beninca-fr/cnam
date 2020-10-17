#! /usr/bin/bash
FILE="$(realpath "${BASH_SOURCE[0]}")"
DIRECTORY="$(dirname "${FILE}")"
cd "${DIRECTORY}"

gedit --new-window thesis/* &
gedit --new-window index.rst build.py common.tex presentation/* &
evince mémoire.pdf présentation.pdf &
