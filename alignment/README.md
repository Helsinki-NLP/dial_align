# alignment

## Edit-distance based alignment methods

* `leven`: Standard Levenshtein distance
* `leven_corpus_pmi`: Weighted Levenshtein distance with PMI costs obtained from the entire corpus
* `leven_doc_pmi`: Weighted Levenshtein distance with PMI costs obtained from each document separately
* `leven_swap`: Levenshtein-Damerau distance, i.e. with transposition/swap

Standard Levenshtein distance uses the Python `edlib` module, all other methods are custom implementations in `levenshtein_align.py`.

For all methods, the `add_adjacent_identicals.py` script is applied to increase alignment coverage.

## Stochastic transducer methods

## Word alignment methods

