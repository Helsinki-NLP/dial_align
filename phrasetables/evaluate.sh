#! /bin/bash -l

echo "" > evaluation.txt
for PROJECT in archimob ndc skn; do
    for ALIGNER in eflomal giza levenshtein; do
        python3 phrt_eval.py "$ALIGNER/$PROJECT/*.phrasetable.gz" >> evaluation.txt
    done
    echo "---------" >> evaluation.txt
done
