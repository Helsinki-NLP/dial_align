#! /usr/bin/env python3

import sys, os, glob, collections

# when running this command, make sure to put the file name pattern into quotes:
# $ python3 makelevpriors.py "m2m/ndc/*.fwd"
pattern = sys.argv[1]
files = glob.glob(pattern)
print(pattern)
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

# this only collects LEX counts
# could be extended to include FERF and FERR counts

pairs = collections.defaultdict(int)
for f in files:
	dirname, basename = os.path.split(f)
	project = dirname.split("/")[-1]
	fileid = basename.split(".")[0]
	srcfilename = f"../../data/{project}/{fileid}.orig"
	tgtfilename = f"../../data/{project}/{fileid}.norm"

	srcfile = open(srcfilename)
	tgtfile = open(tgtfilename)
	alfile = open(f)

	for srcline, tgtline, alline in zip(srcfile, tgtfile, alfile):
		srctokens = srcline.strip().split(" ")
		tgttokens = tgtline.strip().split(" ")
		try:
			alignments = [(int(x.split("-")[0]), (int(x.split("-")[1]))) for x in alline.strip().split(" ")]
		except ValueError:
			print(f"Cannot parse alignment in file {f}:")
			print(alline.strip())
			continue
		
		for i, j in alignments:
			pairs[srctokens[i], tgttokens[j]] += 1
	
	srcfile.close()
	tgtfile.close()
	alfile.close()

outfile = open(sys.argv[2], 'w')
for p in sorted(pairs):
	outfile.write(f"LEX\t{p[0]}\t{p[1]}\t{pairs[p]}\n")
outfile.close()
