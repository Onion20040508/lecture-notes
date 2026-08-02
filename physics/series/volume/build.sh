#!/bin/sh
# One-command volume build. Run from volume/.
set -e
python3 check_crossrefs.py          # refuse to build on citation drift
python3 build_volume.py
cd build
pdflatex -interaction=nonstopmode master.tex > /dev/null
pdflatex -interaction=nonstopmode master.tex > /dev/null
echo "built build/master.pdf"
