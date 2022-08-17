#! /usr/bin/env python3

import re, os, writeData

fillers = {"ja", "mm", "nei", "å", "m", "e", "ok", "da", "jaha", "ja_vel", "hæ", "hm", "oi", "og", "så", "jo", "ehe", "men", "jaha", "...", "?", " mhm", "det", "er", "var", "akkurat", "jeg", "I"}

# Uppercase letters are used for proper names (Italia), speaker abbreviations (F1) and some specific linguistic features (L). We do not change the casing in preprocessing.

# Note: NDC contains vertical bars (for false starts etc.), these should be removed alongside with * and # (but this has not been done for compatibility reasons)

files = os.listdir("ndc_aligned_final")
data = {}
for filename in sorted(files):
	f = open(f"ndc_aligned_final/{filename}")
	n_utt = 0
	n_tok_orig, n_tok_norm = 0, 0
	for line in f:
		elements = line.split("\t")
		speaker = elements[0].strip().replace("<<", "").replace(">>", "")

		orig = elements[1].replace("*", "").replace("#", "")
		# replace references to other informants by I
		orig = re.sub(r'\b\w+_\d\d(\w\w)?\b', 'I', orig)
		# remove existing underscores if they are at the end of a token or constitute a full token
		orig = re.sub(r'_\b', '', orig)
		orig = re.sub(r'\s+', ' ', orig)
		origwords = orig.strip().split(" ")

		norm = elements[2].replace("*", "").replace("#", "")
		# replace references to other informants by I
		norm = re.sub(r'\b\w+_\d\d(\w\w)?\b', 'I', norm)
		# remove existing underscores if they are at the end of a token or constitute a full token
		norm = re.sub(r'_\b', '', norm)
		norm = re.sub(r'\s+', ' ', norm)
		normwords = norm.strip().split(" ")
		if set(normwords) - fillers == set():
			continue

		# there are underscores in both types of transcriptions for multi-word tokens (fårr_eksemmpel, i_mårra, i_værrt_fall, ja_væll) - we just keep the underscores as they are and have them replaced by normal spaces in the postprocessing
		if speaker not in data:
			data[speaker] = []
		n_tok_orig += len(origwords)
		n_tok_norm += len(normwords)
		n_utt += 1
		data[speaker].append((origwords, normwords))
	
	print(f"{filename}: {n_utt} utterances, {n_tok_orig} original words, {n_tok_norm} normalized words")
	f.close()

for s in sorted(data):
	if "_" not in s:
		print(f"{s}: --skipped--")
		continue
	writeData.writeCSMT("ndc", s, data[s])
