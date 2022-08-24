# phrasetables

This directory holds phrase tables extracted for each document using the standard PBSMT phrase table extraction method (the exact command is in `extract_moses.sh`).

Phrase tables are extracted from thee alignment methods:
* `leven`: Standard Levenshtein distance with `add_adjacent_identicals`
* `eflomal`: Eflomal (symmetrized)
* `giza`: Standard GIZA++ (symmetrized)
