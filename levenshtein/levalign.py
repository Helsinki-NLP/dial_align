#! /usr/bin/env python

import edlib, sys

def getLevenAlignment(src, tgt):
	result = edlib.align(tgt, src, task='path')
	align = edlib.getNiceAlignment(result, tgt, src, gapSymbol=" ")
	link_tgt = align['query_aligned']
	link_src = align['target_aligned']
	link_type = align['matched_aligned']
	src_i = 0
	tgt_i = 0
	alignments = []
	for s, t, x in zip(link_src, link_tgt, link_type):
		if x == "|" or x == ".":
			if src_i >= len(src):
				print("Src index out of bounds", src_i, len(src), src)
			elif s != src[src_i]:
				print("Src mismatch:", s, src[src_i], src)
			if tgt_i >= len(tgt):
				print("Tgt index out of bounds", tgt_i, len(tgt), tgt)
			elif t != tgt[tgt_i]:
				print("Tgt mismatch:", t, tgt[tgt_i], tgt)
			alignments.append((src_i, tgt_i))
			src_i += 1
			tgt_i += 1
		elif s == " ":
			tgt_i += 1
		elif t == " ":
			src_i += 1
	return alignments

srcfile = open(sys.argv[1])
tgtfile = open(sys.argv[2])
fwdfile = open(sys.argv[3], 'w')
revfile = open(sys.argv[4], 'w')

for srcline, tgtline in zip(srcfile, tgtfile):
	# assumes that every token is a single character
	src = srcline.strip().replace(" ", "")
	tgt = tgtline.strip().replace(" ", "")

	fwd_align = getLevenAlignment(src, tgt)
	fwd_alignstr = " ".join(["{}-{}".format(x[0], x[1]) for x in fwd_align])
	fwdfile.write(fwd_alignstr + "\n")

	rev_align = getLevenAlignment(tgt, src)
	rev_alignstr =  " ".join(["{}-{}".format(x[1], x[0]) for x in rev_align])
	revfile.write(rev_alignstr + "\n")

srcfile.close()
tgtfile.close()
fwdfile.close()
revfile.close()
