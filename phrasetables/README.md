# phrasetables

This directory holds phrase tables extracted for each document using the standard PBSMT phrase table extraction method (the exact command is in `extract_moses.sh`).

Phrase tables are extracted from these alignment methods:
* `eflomal`: Eflomal (symmetrized)
* `giza`: GIZA++ (symmetrized)
* `fastalign`: fast_align (symmetrized)
* `leven`: Standard Levenshtein distance with `add_adjacent_identicals`
* `leven_corpus_pmi`: Weighted Levenshtein distance with `add_adjacent_identicals`
* `m2m_max11_delXY`: One-to-one stochastic transducer with `add_adjacent_identicals`
* `m2m_max22_delXY_eqmap`: Many-to-many stochastic transducer

The general findings are that `fastalign` and `m2m_max22_delXY_eqmap` perform clearly worst, followed by `giza`. All other methods perform similarly well, but Standard Levenshtein distance generally has the best cost-benefit ratio due to its simplicity.
