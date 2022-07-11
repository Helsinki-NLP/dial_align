#! /usr/bin/env python3

import sys

srctext = open(sys.argv[1])
tgttext = open(sys.argv[2])
fwdalign = open(sys.argv[3])
revalign = open(sys.argv[4])

for src, tgt, fwd, rev in zip(srctext, tgttext, fwdalign, revalign):
	srctokens = src.strip().split(" ")
	tgttokens = tgt.strip().split(" ")
	fwddict = {int(x.split("-")[1]): int(x.split("-")[0]) for x in fwd.strip().split(" ")}
	revdict = {int(x.split("-")[0]): int(x.split("-")[1]) for x in rev.strip().split(" ")}
	firstrow = [str(fwddict.get(i, -1)+1) for i in range(len(tgttokens))]
	secondrow = [str(revdict.get(i, -1)+1) for i in range(len(srctokens))]
	print("1")
	print("{} {}  # {}".format(len(tgttokens), tgt.strip(), " ".join(firstrow)))
	print("{} {}  # {}".format(len(srctokens), src.strip(), " ".join(secondrow)))

srctext.close()
tgttext.close()
fwdalign.close()
revalign.close()
