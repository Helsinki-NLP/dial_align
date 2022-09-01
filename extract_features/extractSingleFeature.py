#! /usr/bin/env python3

import sys, os, gzip, scipy.stats, statistics, collections, csv, numpy
from math import sqrt

aligner = sys.argv[1]
project = sys.argv[2]
feature = sys.argv[3]
if len(sys.argv) > 3:
	threshold = float(sys.argv[4])
else:
	threshold = 0.0
phrtpath = f"../phrasetables/{aligner}/{project}/"

print("Preparing...")
print("  Folder:", phrtpath)
files = os.listdir(phrtpath)
files = [x for x in files if x.endswith(".phrasetable.gz")]
print("  Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

print("Reading phrase tables...")
data = {}
origs = set()
for f in files:
	basename = os.path.basename(f)
	fileid = basename.split(".")[0]
	data[fileid] = {}
	phrtfile = gzip.open(phrtpath + f, 'rt', encoding='utf-8')
	for line in phrtfile:
		elements = line.strip().split(" ||| ")
		orig_str = elements[0].replace(" ", "")
		norm_str = elements[1].replace(" ", "")
		if norm_str != feature:
			continue
		probs = [float(x) for x in elements[2].split(" ")]
		links = [x for x in elements[3].split(" ")]
		counts = [int(x) for x in elements[4].split(" ")]
		if probs[0] < threshold:
			continue
		data[fileid][orig_str] = (probs[0], counts[2])  # prob(orig|norm), count(orig,norm)
		origs.add(orig_str)
print("  Number of variants:", len(origs))
print("  Number of files with variable:", len(data))

outfilename = f"{aligner}.{project}.{feature}.csv"
outfile = open(outfilename, 'w')
writer = csv.writer(outfile)
header = ["Fileid"] + list(sorted(origs))
writer.writerow(header)
for fileid in sorted(data):
	probrow = [data[fileid].get(orig, [0.0, 0])[0] for orig in sorted(origs)]
	writer.writerow([fileid] + probrow)
outfile.close()
