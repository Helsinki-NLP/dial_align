#! /usr/bin/env python3

import sys, os, gzip, scipy.stats, statistics, collections, csv, numpy
from math import sqrt

def hellinger(p,q):
	return sqrt(sum([(sqrt(x)-sqrt(y))**2 for x,y in zip(p,q)]))/sqrt(2)

folder = sys.argv[1]
outfilename = sys.argv[2]

files = os.listdir(folder)
files = [x for x in files if x.endswith(".phrasetable.gz")]
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

print("Reading phrase tables...")
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
fileids.sort()

print("Pruning data...")
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

print("Computing distances...")
distances = collections.defaultdict(list)
sum_array = numpy.zeros((len(fileids), len(fileids)))
count_array = numpy.zeros((len(fileids), len(fileids)))
for n in sorted(data):
	for i in range(len(fileids)):
		# sum_array[i,i] += 0
		count_array[i,i] += 1
		for j in range(i+1, len(fileids)):
			values1 = []
			values2 = []
			for o in data[n]:
				values1.append(data[n][o].get(fileids[i], (0, 0))[0])
				values2.append(data[n][o].get(fileids[j], (0, 0))[0])
			if sum(values1) == 0 or sum(values2) == 0:
				continue
			d = hellinger(values1, values2)
			sum_array[i,j] += d
			sum_array[j,i] += d
			count_array[i,j] += 1
			count_array[j,i] += 1

print(sum_array)
print(count_array)
#assert(numpy.all(count_array == count_array[0,0]))
avg_array = sum_array / count_array

print("Writing results...")
outfile = open(outfilename, 'w')
writer = csv.writer(outfile, delimiter="\t")
row = [""] + fileids
writer.writerow(row)

for fid, data_row in zip(fileids, avg_array):
	writer.writerow([fid] + data_row.tolist())
outfile.close()