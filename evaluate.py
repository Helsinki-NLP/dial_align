#! /usr/bin/env python3

import sys, os, glob

total_alignments = 0
total_src = 0
total_tgt = 0
unaligned_src = 0
unaligned_tgt = 0
same_alignments = 0
diff_alignments = 0
cross_alignments = 0
vc_alignments = 0
errors = 0

vowels = set(list("aeiouäöüyæøå"))
consonants = set(list("bcdfgkpqstvxz"))

# when running this command, make sure to put the file name pattern into quotes:
# $ python3 evaluate.py "m2m/ndc/*.fwd"
pattern = sys.argv[1]
files = glob.glob(pattern)
print(pattern)
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()

for f in files:
	dirname, basename = os.path.split(f)
	project = dirname.split("/")[-1]
	fileid = basename.split(".")[0]
	srcfilename = f"data/{project}/{fileid}.orig"
	tgtfilename = f"data/{project}/{fileid}.norm"

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
			errors += 1
			continue
		
		if max([x[0] for x in alignments]) > len(srctokens) or  max([x[1] for x in alignments]) > len(tgttokens):
			print(f"Cannot parse data in file {f}:")
			print(len(srctokens), srctokens)
			print(len(tgttokens), tgttokens)
			print(alline.strip())
			errors += 1
			continue

		total_src += len(srctokens)
		total_tgt += len(tgttokens)
		total_alignments += len(alignments)
		
		unaligned_src += len(set(range(len(srctokens))) - set([x[0] for x in alignments]))
		unaligned_tgt += len(set(range(len(tgttokens))) - set([x[1] for x in alignments]))

		for a in alignments:
			for b in alignments:
				if b[0] > a[0] and b[1] < a[1]:
					cross_alignments += 1

		for a in alignments:
			if srctokens[a[0]] == tgttokens[a[1]]:
				same_alignments += 1
			else:
				diff_alignments += 1
		
		for a in alignments:
			if srctokens[a[0]].lower() in vowels and tgttokens[a[1]].lower() in consonants:
				vc_alignments += 1
			elif srctokens[a[0]].lower() in consonants and tgttokens[a[1]].lower() in vowels:
				vc_alignments += 1

print("Unaligned source tokens: {:.2f}%".format(unaligned_src/total_src*100))
print("Unaligned target tokens: {:.2f}%".format(unaligned_tgt/total_tgt*100))
print("Alignment to identicals: {:.2f}%".format(same_alignments/total_alignments*100))
print("Alignment to differents: {:.2f}%".format(diff_alignments/total_alignments*100))
print("Crossing alignments:     {:.2f}%".format(cross_alignments/total_alignments*100))
print("Vowel-cons alignments:   {:.2f}%".format(vc_alignments/total_alignments*100))
print("Format errors:   {}".format(errors))
print()
