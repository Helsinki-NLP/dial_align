# alignment

## Edit-distance based alignment methods

* `leven`: Standard Levenshtein distance
* `leven_corpus_pmi`: Weighted Levenshtein distance with PMI costs obtained from the entire corpus
* `leven_doc_pmi`: Weighted Levenshtein distance with PMI costs obtained from each document separately
* `leven_swap`: Levenshtein-Damerau distance, i.e. with transposition/swap

Standard Levenshtein distance uses the Python `edlib` module, all other methods are custom implementations in `levenshtein_align.py`.

For all methods, the `add_adjacent_identicals.py` script is applied to increase alignment coverage.

## Stochastic transducer methods

* `m2m_max11_delXY`: Single-character transducer allowing deletions and insertions (i.e. Levenshtein distance with EM-learned weights).
* `m2m_max11_delXY_init`: Same as above, initialized with Levenshtein weights.
* `m2m_max22_delXY`: Extension allowing bigrams on either source or target side, but not both.
* `m2m_max22_delXY_eqmap`: Extension allowing bigrams on either source or target side or both.
* `m2m_max22_eqmap`: Extension allowing bigrams on either source or target side or both, but disallowing insertions and deletions.
* `m2m_max22`: Extension allowing bigrams on either source or target side, but not both. Insertions and deletions are also disallowed.
* `m2m_asym_max21_max12_delXY`: Runs the max22_delXY model twice, once restricting source to unigrams, once restricting target to unigrams. Results are then symmetrized.

All experiments are based on the [m2m-aligner](https://github.com/letter-to-phoneme/m2m-aligner) toolkit by Jiampojamarn et al.

## Word alignment methods

