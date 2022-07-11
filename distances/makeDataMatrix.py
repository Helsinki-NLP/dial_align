#! /usr/bin/env python3

import sys, os, gzip, csv

folder = sys.argv[1]
outfilename = sys.argv[2]

files = os.listdir(folder)
files = [x for x in files if x.endswith(".phrasetable.gz")]
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

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
		if norm_str not in data:
			data[norm_str] = {}
		if orig_str not in data[norm_str]:
			data[norm_str][orig_str] = {}
		data[norm_str][orig_str][fileid] = (probs[0], counts[2])  # prob(orig|norm), count(orig,norm)

# remove keys with single variant and keys with single text and keys with < 100 occurrences
OCC_THRESH = 100
for n in list(data.keys()):
	if len(data[n]) == 1:
		del data[n]
		continue
	texts = set()
	for o in data[n]:
		texts.update(data[n][o].keys())
	if len(texts) == 1:
		del data[n]
		continue
	sumocc = sum([data[n][o][i][1] for o in data[n] for i in data[n][o]])
	if sumocc < 100:
		del data[n]
# also remove origs that have one single (or very few) occurrences?

outfile = open(outfilename, 'w')
writer = csv.writer(outfile, delimiter="\t")
row = ["FILEID"]
for n in sorted(data):
	for o in sorted(data[n]):
		row.append(f"{n}:{o}")
writer.writerow(row)
print("Features:", len(row)-1)

for f in sorted(fileids):
	row = [f]
	for n in sorted(data):
		for o in sorted(data[n]):
			row.append(data[n][o].get(f, (0,0))[0])
	writer.writerow(row)
outfile.close()
