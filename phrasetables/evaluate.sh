#! /bin/bash -l

echo "" > evaluation.txt
for ALIGNER in giza eflomal fastalign leven leven_corpus_pmi m2m_max11_delXY m2m_max22_delXY_eqmap; do
    echo "---------" >> evaluation.txt
    echo "$ALIGNER" >> evaluation.txt
    echo "---------" >> evaluation.txt
    echo "" >> evaluation.txt
    for PROJECT in archimob ndc skn; do
        echo $ALIGNER $PROJECT
        python3 phrt_eval.py "$ALIGNER/$PROJECT/*.phrasetable.gz" >> evaluation.txt
    done
done
