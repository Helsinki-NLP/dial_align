# Extraction of manually defined features and feature sets

`extractSingleFeature.py` extracts the probability distributions over variants and files for a given feature (a feature is an n-gram that occurs on the normalized side of the phrase table).

`extractFeatureSet.py` extracts the probability distributions over variants and files for a given *set of features*. It computes pairwise Hellinger distance for each pair of files and for each feature, then averages the different distance matrices for the different features to provide one single distance matrix.


The script `extract_all.sh` gives some example runs. The resulting csv files are also part of this directory.
