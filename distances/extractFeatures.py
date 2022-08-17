#! /usr/bin/env python3

import sys, os, gzip, scipy.stats, statistics, collections, csv, numpy
from math import sqrt

def hellinger(p,q):
	return sqrt(sum([(sqrt(x)-sqrt(y))**2 for x,y in zip(p,q)]))/sqrt(2)

def overlap(n1, n2, data):
	if n2 in n1 and n2 != n1:
		# n2 is a substring of n1
		if n1.endswith(n2):
			prefix = n1.replace(n2, "")
			extended_o2_keys = [prefix + o2 for o2 in data[n2]]
			#print(n1, n2, "prefix:", prefix, extended_o2_keys, sorted(list(data[n2].keys())))
		elif n1.startswith(n2):
			suffix = n1.replace(n2, "")
			extended_o2_keys = [o2 + suffix for o2 in data[n2]]
			#print(n1, n2, "suffix:", suffix, extended_o2_keys, sorted(list(data[n2].keys())))
		else:
			return False
		# print(n1, data[n1].keys())
		# print(n2, data[n2].keys())
		# print(extended_o2_keys)
		# print("------")
		if sorted(list(data[n1].keys())) == sorted(extended_o2_keys):
			#print(n1, n2, "overlap", extended_o2_keys, sorted(list(data[n1].keys())))
			return True
	return False


def displayKey(k, d):
	for o in d:
		s = ""
		for i in d[o]:
			s += "{}:{} ".format(i, d[o][i][1])
		print("  ", o, s)

folder = sys.argv[1]

print("Preparing...")
print("  Folder:", folder)
files = os.listdir(folder)
files = [x for x in files if x.endswith(".phrasetable.gz")]
print("  Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

VAR_OCC_THRESH = 10
MAX_N_LEN = 1
print("Reading phrase tables (remove variants with <{} variants)...".format(VAR_OCC_THRESH))
data = {}
fileids = []
for f in files:
	basename = os.path.basename(f)
	fileid = basename.split(".")[0]
	fileids.append(fileid)
	phrtfile = gzip.open(folder + "/" + f, 'rt', encoding='utf-8')
	for line in phrtfile:
		elements = line.strip().split(" ||| ")
		orig_str = elements[0].replace(" ", "")
		norm_str = elements[1].replace(" ", "")
		probs = [float(x) for x in elements[2].split(" ")]
		links = [x for x in elements[3].split(" ")]
		counts = [int(x) for x in elements[4].split(" ")]
#		if len(orig_str) > MAX_N_LEN or len(norm_str) > MAX_N_LEN:
#			continue
		if counts[2] < VAR_OCC_THRESH:
			continue
		if norm_str not in data:
			data[norm_str] = {}
		if orig_str not in data[norm_str]:
			data[norm_str][orig_str] = {}
		data[norm_str][orig_str][fileid] = (probs[0], counts[2])  # prob(orig|norm), count(orig,norm)
fileids.sort()
print("  Number of keys:", len(data))
print("  Number of key/variant pairs:", sum([len(data[x]) for x in data]))

# This removes the longer of the two keys
# We might get better results by removing the shorter one instead
MAX_NGRAM=6
for ngram in range(MAX_NGRAM, 1, -1):
	print("Removing overlapping keys of length {}...".format(ngram))
	overlap_keys = []
	for n1 in [x for x in data if len(x) == ngram]:
		for n2 in [x for x in data if len(x) == ngram-1]:
			if overlap(n1, n2, data):
				overlap_keys.append(n1)		# remove the longer of the two strings
	print("  Overlaps:", len(overlap_keys))
	for k in overlap_keys:
		if k in data:
			del data[k]
	print("  Number of keys:", len(data))
	print("  Number of key/variant pairs:", sum([len(data[x]) for x in data]))

print("Removing keys with single variant...")
for n in list(data.keys()):
	if len(data[n]) == 1:
		del data[n]
print("  Number of keys:", len(data))
print("  Number of key/variant pairs:", sum([len(data[x]) for x in data]))

TEXT_THRESH = 10
print("Removing keys with <{} texts...".format(TEXT_THRESH))
for n in list(data.keys()):
	texts = set()
	for o in data[n]:
		texts.update(data[n][o].keys())
	if len(texts) < TEXT_THRESH:
		del data[n]
print("  Number of keys:", len(data))
print("  Number of key/variant pairs:", sum([len(data[x]) for x in data]))

print("Computing distances...")
skipped = 0
means = {}
stdevs = {}
for n in sorted(data):
	distance_list = []
	for i in range(len(fileids)):
		for j in range(i+1, len(fileids)):
			values1 = []
			values2 = []
			for o in data[n]:
				if fileids[i] in data[n][o] or fileids[j] in data[n][o]:
					values1.append(data[n][o].get(fileids[i], (0, 0))[0])
					values2.append(data[n][o].get(fileids[j], (0, 0))[0])
			if len(values1) < 2:
				skipped += 1
				continue
			d = hellinger(values1, values2)
			distance_list.append(d)
	if distance_list == []:
		continue
	#print(n, min(distance_list), max(distance_list), statistics.mean(distance_list))
	means[n] = statistics.mean(distance_list)
	stdevs[n] = statistics.variance(distance_list)
print("  Skipped comparisons:", skipped)

print()
print("MEANS")
i = 0
for k, v in sorted(means.items(), key=lambda x: x[1], reverse=True):
	i += 1
	print(i, k, v)
	#displayKey(k, data[k])
	print("  ", " ".join(data[k].keys()))
	print()
	if i > 20:
		break

print()
print("VARIANCES")
i = 0
for k, v in sorted(stdevs.items(), key=lambda x: x[1], reverse=True):
	i += 1
	print(i, k, v)
	#displayKey(k, data[k])
	print("  ", " ".join(data[k].keys()))
	print()
	if i > 20:
		break
