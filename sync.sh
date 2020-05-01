#! /bin/bash
FILE="$(realpath "${BASH_SOURCE[0]}")"
DIRECTORY="$(dirname "${FILE}")"

cd "${DIRECTORY}"

rsync \
--archive \
--progress \
--verbose \
--delete-before \
out/ \
marc-beninca.fr:/ssd/projects/public/marc-beninca.fr/cnam/out/
