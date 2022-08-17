#! /usr/bin/env python

import edlib, sys, math
import numpy as np

#####################################

# https://stackoverflow.com/questions/66636450/how-to-implement-alignment-through-traceback-for-levenshtein-edit-distance

def backtrace(first, second, matrix, costs):
	f = [char for char in first]
	s = [char for char in second]
	new_f, new_s = [], []
	new_t = []
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
				return new_f, new_s, new_t

		# Exit the loop
		if row == 0 or col == 0:
			return new_f, new_s, new_t


def word_edit_distance(x, y, costs):
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
	
	
	new_x, new_y, new_t = backtrace(x, y, distance, costs)
	return "".join(new_x[::-1]), "".join(new_y[::-1]), "".join(new_t[::-1])

######################################

def buildAlignment(orig_src, link_src, orig_tgt, link_tgt, link_type):
	src_i = 0
	tgt_i = 0
	alignments = []
	for s, t, x in zip(link_src, link_tgt, link_type):
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

def getLevenAlignment(src, tgt):
	result = edlib.align(tgt, src, task='path')
	align = edlib.getNiceAlignment(result, tgt, src, gapSymbol=" ")
	link_tgt = align['query_aligned']
	link_src = align['target_aligned']
	link_type = align['matched_aligned']
	return link_src, link_tgt, link_type

def align_edlib(src, tgt):
	result = edlib.align(tgt, src, task='path')
	align = edlib.getNiceAlignment(result, tgt, src, gapSymbol=" ")
	alignments = buildAlignment(src, align['target_aligned'], tgt, align['query_aligned'], align['matched_aligned'])
	return alignments

def align_own(src, tgt, costs):
	s, t, a = word_edit_distance(src, tgt, costs)
	alignments = buildAlignment(src, s, tgt, t, a)
	return alignments

def loadCosts(costsfile):
	costs = {}
	for line in costsfile:
		elem = line.strip().split(" ")
		src = elem[0].replace("@", "")
		tgt = elem[1].replace("@", "")
		val = float(elem[2])
		costs[src, tgt] = val
	return costs

def makeLevenCosts(src, tgt):
	costs = {}
	for s in src:
		for t in tgt:
			if s == t:
				costs[s,t] = 0
			else:
				costs[s,t] = 1
			costs['',t] = 1
		costs[s,''] = 1
	return costs


srcfile = open(sys.argv[1])
tgtfile = open(sys.argv[2])
costsfile = open(sys.argv[3])
outfile = open(sys.argv[4], 'w')

costs = loadCosts(costsfile)
for srcline, tgtline in zip(srcfile, tgtfile):
	# assumes that every token is a single character
	src = srcline.strip().replace(" ", "")
	tgt = tgtline.strip().replace(" ", "")
	alignment = align_own(src, tgt, costs)
	alignstr = " ".join(["{}-{}".format(x[0], x[1]) for x in alignment])
	outfile.write(alignstr + "\n")

srcfile.close()
tgtfile.close()
costsfile.close()
outfile.close()
