#! /usr/bin/env python3

import sys, os, gzip, numpy, pandas
import scipy.spatial.distance as ssd

aligner = sys.argv[1]
project = sys.argv[2]
threshold = float(sys.argv[3])
features = sys.argv[4:]
phrtpath = f"../phrasetables/{aligner}/{project}/"

print("Preparing...")
print("  Folder:", phrtpath)
files = os.listdir(phrtpath)
files = [x for x in files if x.endswith(".phrasetable.gz")]
print("  Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()
print("  Target features:", features)
print("  Threshold:", threshold)

print("Reading phrase tables...")
datadict = {}
for f in files:
	basename = os.path.basename(f)
	fileid = basename.split(".")[0]
	phrtfile = gzip.open(phrtpath + f, 'rt', encoding='utf-8')
	for line in phrtfile:
		elements = line.strip().split(" ||| ")
		orig_str = elements[0].replace(" ", "")
		norm_str = elements[1].replace(" ", "")
		if norm_str not in features:
			continue
		probs = [float(x) for x in elements[2].split(" ")]
		links = [x for x in elements[3].split(" ")]
		counts = [int(x) for x in elements[4].split(" ")]
		if probs[0] < threshold:
			continue
		if norm_str not in datadict:
			datadict[norm_str] = {}
		if fileid not in datadict[norm_str]:
			datadict[norm_str][fileid] = {}
		datadict[norm_str][fileid][orig_str] = probs[0] # prob(orig|norm)

print("Computing distances...")
data_matrices = {}
dist_matrices = {}
fileids = None
for n in datadict:
	data_matrices[n] = pandas.DataFrame(datadict[n]).fillna(0).transpose().sort_index(axis=0)
	fileids = data_matrices[n].index.values
	print(f"  {n}: {data_matrices[n].shape[0]} texts, {data_matrices[n].shape[1]} variants")
	# Hellinger distance
	dist_matrices[n] = ssd.squareform(ssd.pdist(numpy.sqrt(data_matrices[n].values)))/numpy.sqrt(2)

print("Aggregating distances...")
for n in dist_matrices:
	print(" ", n, dist_matrices[n].shape)
dist_all = numpy.array([dist_matrices[n] for n in dist_matrices])
dist_final = numpy.mean(dist_all, axis=0)

print("Writing results...")
featurestr = "_".join(features)
outfilename = f"dist.{aligner}.{project}.{featurestr}.csv"
outfile = open(outfilename, 'w')
df = pandas.DataFrame(data=dist_final, index=fileids, columns=fileids)
df.to_csv(outfilename, index=True)
