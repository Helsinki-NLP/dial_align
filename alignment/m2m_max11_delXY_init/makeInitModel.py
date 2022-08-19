#! /usr/bin/env python3

import sys, glob

modelGlob = sys.argv[1]
files = glob.glob(modelGlob)
print(modelGlob)
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

vocab = set()
for fn in files:
	f = open(fn, 'r')
	for line in f:
		elements = line.strip().split("\t")
		vocab.add(elements[0])
		vocab.add(elements[1])
	f.close()

idWeight = 0.5
diffWeight = (1.0 - idWeight) / (len(vocab)-1)

outfile = open(sys.argv[2], 'w')
for v1 in sorted(vocab):
	for v2 in sorted(vocab):
		w = idWeight if v1 == v2 else diffWeight
		outfile.write(f"{v1}\t{v2}\t{w:.6f}\n")
outfile.close()
