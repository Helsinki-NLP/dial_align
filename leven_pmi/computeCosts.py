#! /usr/bin/env python3

import collections, sys, os, math

paircounts = collections.defaultdict(int)
origcounts = collections.defaultdict(int)
normcounts = collections.defaultdict(int)

project = sys.argv[1]
levfolder = sys.argv[2]

files = [x.replace(".fwd", "") for x in os.listdir(f"../{levfolder}/{project}") if x.endswith(".fwd")]
for f in files:
	of = open(f"../data/{project}/{f}.orig")
	nf = open(f"../data/{project}/{f}.norm")
	af = open(f"../{levfolder}/{project}/{f}.fwd")

	for origline, normline, alignline in zip(of, nf, af):
		origs = origline.strip().split(" ")
		norms = normline.strip().split(" ")
		aligns = alignline.strip().split(" ")
		alignments = [(int(x.split("-")[0]), int(x.split("-")[1])) for x in aligns]
		covered_orig, covered_norm = set(), set()
		for a in alignments:
			paircounts[origs[a[0]], norms[a[1]]] += 1
			covered_orig.add(a[0])
			covered_norm.add(a[1])
		for i in range(len(origs)):
			if i not in covered_orig:
				paircounts[origs[i], '@'] += 1
				origcounts['@'] += 1
		for j in range(len(norms)):
			if j not in covered_norm:
				paircounts['@', norms[j]] += 1
				normcounts['@'] += 1
		for o in origs:
			origcounts[o] += 1
		for n in norms:
			normcounts[n] += 1
	
	of.close()
	nf.close()
	af.close()

# http://www.let.rug.nl/nerbonne/teach/dialectology/LOT-sheets/pmi-accents-wieling-2012.pdf
sum_pairs = sum(paircounts.values())
sum_origs = sum(origcounts.values())
sum_norms = sum(normcounts.values())
pmi = {}
for x, y in paircounts:
	p_x_y = paircounts[x,y] / sum_pairs
	p_x = origcounts[x] / sum_origs
	p_y = normcounts[y] / sum_norms
	pmi[x,y] = math.log(p_x_y / (p_x * p_y))

min_pmi = min(pmi.values())
max_pmi = max(pmi.values())

costs = {}
for k in pmi:
	costs[k] = 1 - ((pmi[k]-min_pmi) / (max_pmi-min_pmi))
# add unseen combinations
for o in origcounts:
	for n in normcounts:
		if (o, n) not in costs and (o, n) != ("@", "@"):
			costs[o, n] = 1.0

for x, y in sorted(costs):
	print(f"{x} {y} {costs[x,y]:.6f}")
