#! /usr/bin/env python

import argparse, edlib, sys, math
import numpy as np

###################################################

# https://stackoverflow.com/questions/66636450/how-to-implement-alignment-through-traceback-for-levenshtein-edit-distance

def backtrace(first, second, matrix, costs):
	f = [char for char in first]
	s = [char for char in second]
	new_f, new_s = [], []
	new_t = []
	new_list = []	# builds Pharaoh-style alignment pairs directly
	row = len(f)
	col = len(s)

	while True:
		r = matrix[row][col]
		a = matrix[row - 1][col]
		b = matrix[row - 1][col - 1]
		c = matrix[row][col - 1]

		if math.isclose(r, b + costs[f[row-1], s[col-1]], abs_tol=10**-4):
			# when diagonal backtrace substitution or no substitution
			new_f = [f[row - 1]] + new_f
			new_s = [s[col - 1]] + new_s
			if f[row-1] == s[col-1]:
				new_t = ["|"] + new_t
			else:
				new_t = ["."] + new_t
			new_list.append((row, col))
			row, col = row - 1, col - 1

		else:
			# either deletion or insertion, find if minimum is up or left
			if math.isclose(r, a + costs[f[row-1],''], abs_tol=10**-4):
				new_f = [f[row - 1]] + new_f
				new_s = [" "] + new_s
				new_t = [" "] + new_t
				row, col = row - 1, col

			elif math.isclose(r, c + costs['',s[col-1]], abs_tol=10**-4):
				new_f = [" "] + new_f
				new_s = [s[col - 1]] + new_s
				new_t = [" "] + new_t
				row, col = row, col - 1
			
			else:
				print("No option applies, give up on sentence")
				print(r, a + costs[f[row-1],''], c + costs['',s[col-1]], b + costs[f[row-1], s[col-1]])
				return new_f, new_s, new_t, new_list

		# Exit the loop
		if row == 0 or col == 0:
			return new_f, new_s, new_t, new_list


def weighted_levenshtein_distance(x, y, costs):
	# reverse strings to simulate attachment behavior of edlib
	x = x[::-1]
	y = y[::-1]
	rows = len(x) + 1
	cols = len(y) + 1
	distance = np.zeros((rows, cols), dtype=np.float32)

	for i in range(1, rows):
		distance[i][0] = distance[i-1][0] + costs[x[i-1], '']		# del
	for k in range(1, cols):
		distance[0][k] = distance[0][k-1] + costs['', y[k-1]]		# ins

	for col in range(1, cols):
		for row in range(1, rows):
			distance[row][col] = min(distance[row-1][col] + costs[x[row-1], ''],	# del
									 distance[row][col-1] + costs['', y[col-1]],	# ins
									 distance[row-1][col-1] + costs[x[row-1], y[col-1]])	# sub
	
	
	new_x, new_y, new_t, new_list = backtrace(x, y, distance, costs)
	new_list = [(rows-r-1, cols-c-1) for (r, c) in new_list]
	return "".join(new_x[::-1]), "".join(new_y[::-1]), "".join(new_t[::-1]), new_list

###################################################

def build_alignment(orig_src, link_src, orig_tgt, link_tgt, link_type):
	src_i = 0
	tgt_i = 0
	alignments = []
	for s, t, x in zip(link_src, link_tgt, link_type):
		# link type: | = identity, . = substitution, (space) = ins or del
		if x == "|" or x == ".":
			if src_i >= len(orig_src):
				print("Src index out of bounds", src_i, len(orig_src), orig_src)
			elif s != orig_src[src_i]:
				print("Src mismatch:", s, orig_src[src_i], orig_src)
			if tgt_i >= len(orig_tgt):
				print("Tgt index out of bounds", tgt_i, len(orig_tgt), orig_tgt)
			elif t != orig_tgt[tgt_i]:
				print("Tgt mismatch:", t, orig_tgt[tgt_i], orig_tgt)
			alignments.append((src_i, tgt_i))
			src_i += 1
			tgt_i += 1
		elif s == " ":
			tgt_i += 1
		elif t == " ":
			src_i += 1
	return alignments


def align_edlib(src, tgt):
	result = edlib.align(tgt, src, task='path')
	align = edlib.getNiceAlignment(result, tgt, src, gapSymbol=" ")
	alignments = build_alignment(src, align['target_aligned'], tgt, align['query_aligned'], align['matched_aligned'])
	return alignments


def align_weighted(src, tgt, costs):
	s, t, a, l = weighted_levenshtein_distance(src, tgt, costs)
	#alignments = build_alignment(src, s, tgt, t, a)
	return l


def load_costs(costsfile):
	fwd_costs = {}
	rev_costs = {}
	for line in costsfile:
		elem = line.strip().split(" ")
		src = elem[0].replace("@", "")
		tgt = elem[1].replace("@", "")
		val = float(elem[2])
		fwd_costs[src, tgt] = val
		rev_costs[tgt, src] = val
	return fwd_costs, rev_costs


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Character alignment with Levenshtein distance')
	parser.add_argument('-method', choices=['edlib', 'weighted', 'damerau'], help='Algorithm used for the alignment', required=True)
	parser.add_argument('-src', type=argparse.FileType('r'), help='File with the source data', required=True)
	parser.add_argument('-tgt', type=argparse.FileType('r'), help='File with the target data', required=True)
	parser.add_argument('-fwd', type=argparse.FileType('w'), help='File into which forward alignments are written (optional)')
	parser.add_argument('-rev', type=argparse.FileType('w'), help='File into which reverse alignments are written (optional)')
	parser.add_argument('-costs', type=argparse.FileType('r'), help='File with the transition costs')
	args = parser.parse_args()

	if args.costs is not None:
		fwd_costs, rev_costs = load_costs(args.costs)

	for srcline, tgtline in zip(args.src, args.tgt):
		# assumes that every token is a single character
		src = srcline.strip().replace(" ", "")
		tgt = tgtline.strip().replace(" ", "")

		if args.fwd is not None:
			if args.method == 'edlib':
				fwd_align = align_edlib(src, tgt)
			elif args.method == 'weighted':
				fwd_align = align_weighted(src, tgt, fwd_costs)
			else:
				raise NotImplementedError(args.method)
			fwd_alignstr = " ".join(["{}-{}".format(x[0], x[1]) for x in fwd_align])
			args.fwd.write(fwd_alignstr + "\n")
		
		if args.rev is not None:
			if args.method == 'edlib':
				rev_align = align_edlib(tgt, src)
			elif args.method == 'weighted':
				rev_align = align_weighted(tgt, src, rev_costs)
			else:
				raise NotImplementedError(args.method)
			rev_alignstr =  " ".join(["{}-{}".format(x[1], x[0]) for x in rev_align])
			args.rev.write(rev_alignstr + "\n")
