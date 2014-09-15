#! /usr/bin/env python
"""
Script for splitting pdf, .doc and .docx files.


Copyright 2014 David Simic

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
from pyPdf import PdfFileWriter, PdfFileReader
from subprocess import call
import traceback
import sys
import os


# ghostscript command schema
GS_CMD = "gs -o %s -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress %s"
# unoconv command schema
UNOCONV_CMD = 'unoconv -f pdf %s'


def fix_pdf(inputfile):
    """
    Attempt to fix a pdf using ghostscript.
    """
    # attempt to fix using ghostscript on linux
    inputfile_fixed = inputfile[:-4] + ".fixed.pdf"
    try:
        print "INFO: Calling ghostscript ..."
        cmd = GS_CMD % (inputfile_fixed, inputfile)
        print ">> %s" % cmd
        call(cmd.split())
    except OSError, e:
        print traceback.format_exc()
        print sys.exc_info()[0]
        print >> sys.stderr, \
                "ERROR: Call to ghostscript went wrong, "+\
                "check if installed."
        return
    # hopefully will work this time
    inputpdf = PdfFileReader(open(inputfile_fixed, "rb"))
    # remove trace of fixed
    os.remove(inputfile_fixed)
    return inputpdf


def read_pdf(inputfile):
    """
    If read fails, attempts to fixed pdf using ghostscript.
    """
    try:
        inputpdf = PdfFileReader(open(inputfile, "rb"))
        return inputpdf
    except:
        print "INFO: PDF broken, attempting to fix using ghostscript."
        # attempt to fix using ghostscript on linux
        inputpdf = fix_pdf(inputfile)
        return inputpdf


def split_pdf(inputfile):
    """
    Splits an input pdf doc given filename. For simplicity,
    must end in *.pdf
    """
    # enforce suffix
    assert inputfile.split(".")[-1] == "pdf"
    # read file
    inputpdf = read_pdf(inputfile)
    # check None
    if inputpdf is None:
        return
    # init outfiles
    outpdfs = []
    # process into pages and save each page
    for i in xrange(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        outpdfs.append((i, output))
    return outpdfs


def libre_doc_to_pdf(inputfile):
    """
    Converts ms .doc and .docx files to pdf
    using libreoffice daemon via the linux util unoconv.
    """
    # convert ms .doc and .docx to pdf using libreoffice daemon
    try:
        print "INFO: Calling unoconv ..."
        cmd = UNOCONV_CMD % inputfile
        print ">> %s" % cmd
        call(cmd.split())
    except OSError, e:
        print traceback.format_exc()
        print sys.exc_info()[0]
        print >> sys.stderr, \
                "ERROR: Call to unoconv went wrong, "+\
                "check if installed."
        return

    if "." not in inputfile:
        pdffile = inputfile + ".pdf"
    else:
        pdffile = '.'.join(inputfile.split(".")[:-1]) + ".pdf"
    return pdffile


def split_doc(inputfile):
    """
    Splits pdf or libreoffice importable doc (.doc, .docx, etc),
    into pdfs, one pdf per page.
    """
    inputfile_suff = inputfile.split(".")[-1]
    if inputfile_suff != "pdf":
        inputfile = libre_doc_to_pdf(inputfile)
    return split_pdf(inputfile)


def write_pdfs(inputfile, pages, outdir=None):
    """
    Write PDFs to disk.
    """
    if outdir is not None and not os.path.exists(outdir):
        os.makedirs(outdir)
    for i, output in pages:
        outfile = inputfile[:-4] + "_%s.pdf" % i
        if outdir is not None:
            outfile = outdir + "/" + os.path.basename(outfile)
        with open(outfile, "wb") as output_stream:
            output.write(output_stream)
    return


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description="A script for splitting" +
        " a .pdf, .doc, .docx and other documents into one pdf per page")
    parser.add_argument("docfile", help="path to docfile",
                        type=str)
    parser.add_argument("--outdir", help="override default outdir" +\
            "(default is same dir as docfile)",
            type=str, required=None, default=None)
    args = parser.parse_args()

    # split pages
    pages = split_doc(args.docfile)

    # check if page splitsucceded.
    if pages is None:
        print "ERROR: doc could not be split. exiting."
        sys.exit(1)

    # page split succeded, write pages.
    write_pdfs(args.docfile, pages, outdir=args.outdir)

    # exit normally
    sys.exit()
