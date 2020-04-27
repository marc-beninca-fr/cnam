#! /usr/bin/python3 -B

import os
import shutil

import sphinx

INPUT = ["cnam"]
OUTPUT = "out"


def others():
    import cnam.travaux.blanc.build as blanc
    blanc.main()


def main():
    file = os.path.realpath(__file__)
    directory = os.path.dirname(file)
    output_directory = os.path.join(directory, OUTPUT)
    shutil.rmtree(output_directory, ignore_errors=True)
    for doc in INPUT:
        arguments = [
            "-E",
            "-j", "2",
            "-b", "html",
            "-D", "project={}".format(doc),
            "-D", "master_doc={}".format("index"),
            "-D", "html_theme={}".format("sphinx_rtd_theme"),
            # "-C",
            "-c", directory,
            os.path.join(directory, doc),
            os.path.join(output_directory, doc),
        ]
        sphinx.build_main(arguments)
    others()


if __name__ == "__main__":
    main()
