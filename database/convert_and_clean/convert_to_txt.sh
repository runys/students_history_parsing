#!/bin/bash

for pdf in *.pdf; do
    pdftotext "$pdf";
done
