docsplit
========

Python script for splitting .pdf, .doc, .docx and a few other document types into single page pdfs.

It depends on ghostscript (for fixing pdfs) and unoconv (a command line 'front-end' for accessing libreoffice). 

Install
-------

If you are on Ubuntu just run the ./install_deps.sh script in sudo. If you are on another Linux distro, install the dependencies described in install_deps.sh.


Usage
-----

For usage, simply run docsplit.py:

python docsplit.py --help

usage: docsplit.py [-h] [--outdir OUTDIR] docfile

A script for splitting a .pdf, .doc, .docx and other documents into one pdf
per page

positional arguments:
  docfile          path to docfile

optional arguments:
  -h, --help       show this help message and exit
  --outdir OUTDIR  override default outdir(default is same dir as docfile)

Examples
--------

After all dependencies have been install and you ahve verified that

python docsplit.py --help

does not crash and burn, run "./examples.sh" for a few examples. This script
will split the docs in the ./test/ subdir. 
