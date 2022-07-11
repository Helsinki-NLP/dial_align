#! /usr/bin/env python3

import sys, os, glob, gzip, json, collections, statistics

# when running this command, make sure to put the file name pattern into quotes:
# $ python3 evaluate.py "eflomal/ndc/*.phrasetable.gz"
pattern = sys.argv[1]
files = glob.glob(pattern)
print(pattern)
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

data = {}
for f in files:
	dirname, basename = os.path.split(f)
	project = dirname.split("/")[-1]
	fileid = basename.split(".")[0]
	phrtfile = gzip.open(f, 'rt', encoding='utf-8')
	for line in phrtfile:
		elements = line.strip().split(" ||| ")
		orig_str = elements[0].replace(" ", "")
		norm_str = elements[1].replace(" ", "")
		probs = [float(x) for x in elements[2].split(" ")]
		links = [x for x in elements[3].split(" ")]
		counts = [int(x) for x in elements[4].split(" ")]
		if norm_str not in data:
			data[norm_str] = {}
		if orig_str not in data[norm_str]:
			data[norm_str][orig_str] = {}
		data[norm_str][orig_str][fileid] = counts[2]

OCC_THRESH = 100
HALF_THRESH = int(len(files) / 2)
orig_counts = []
single_orig_count = 0
orig_distr = collections.defaultdict(int)
text_counts = []
single_text_count = 0
half_text_count = 0
text_distr = collections.defaultdict(int)
norm_count = len(data)
low_occ_count = 0
count_distr = collections.defaultdict(int)
all_filters = 0

for n in data:
	n_orig = len(data[n])
	orig_counts.append(n_orig)
	if n_orig == 1:
		single_orig_count += 1
	orig_distr[n_orig] += 1

	texts = set()
	for o in data[n]:
		texts.update(data[n][o].keys())
	n_texts = len(texts)
	text_counts.append(n_texts)
	if n_texts == 1:
		single_text_count += 1
	if n_texts < HALF_THRESH:
		half_text_count += 1
	text_distr[n_texts] += 1
	
	variant_counts = sum([data[n][o][i] for o in data[n] for i in data[n][o]])
	if variant_counts < OCC_THRESH:
		low_occ_count += 1
	count_distr[variant_counts] += 1

	if n_orig == 1 or n_texts == 1 or variant_counts < OCC_THRESH or n_texts < HALF_THRESH:
		all_filters += 1
	
print("Norm keys:                {}".format(norm_count))
print("Avg variants per key:     {:.4f}".format(statistics.mean(orig_counts)))
print("Avg texts per key:        {:.4f}".format(statistics.mean(text_counts)))
print("Keys with single variant: {:.4f} %".format(100 * single_orig_count / norm_count))
print("Keys with single text:    {:.4f} %".format(100 * single_text_count / norm_count))
print("Keys with <{} texts:      {:.4f} %".format(HALF_THRESH, 100 * half_text_count / norm_count))
print("Keys with <{} occur.:     {:.4f} %".format(OCC_THRESH, 100 * low_occ_count / norm_count))
print("Keys with any filter:     {:.4f} %".format(100 * all_filters / norm_count))

# remove keys with single variant and keys with single text
for n in list(data.keys()):
	if len(data[n]) == 1:
		del data[n]
	if n not in data:
		continue
	texts = set()
	for o in data[n]:
		texts.update(data[n][o].keys())
	if len(texts) == 1:
		del data[n]

# redo the counts
orig_counts = []
text_counts = []
norm_count = len(data)

for n in data:
	n_orig = len(data[n])
	orig_counts.append(n_orig)
	texts = set()
	for o in data[n]:
		texts.update(data[n][o].keys())
	n_texts = len(texts)
	text_counts.append(n_texts)

print("After singleton removal:")
print("Norm keys:                {}".format(norm_count))
print("Avg variants per key:     {:.4f}".format(statistics.mean(orig_counts)))
print("Avg texts per key:        {:.4f}".format(statistics.mean(text_counts)))
print()

# print("Occurrence count distribution:")
# for i in sorted(count_distr, reverse=True):
# 	print(i, count_distr[i])
# print()
# print("Variant distribution:")
# for i in sorted(orig_distr, reverse=True):
# 	print(i, orig_distr[i])
# print()
# print("Text distribution:")
# for i in sorted(text_distr, reverse=True):
# 	print(i, text_distr[i])
# print()

# print(json.dumps(data, sort_keys=True, indent=4))
