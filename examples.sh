OUTROOT=./test/tmp/
# clean OUTROOT
if [ -d $OUTROOT ]; then
    rm -rf $OUTROOT
fi

python docsplit.py test/a.pdf --outdir $OUTROOT/a/ 

python docsplit.py test/b.doc --outdir $OUTROOT/b/ 

python docsplit.py test/c.docx --outdir $OUTROOT/c/ 
