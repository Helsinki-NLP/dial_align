#! /bin/bash -l

#for PROJECT in archimob ndc skn; do
for PROJECT in skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls ../data/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python3 ../dtw.py ../data/$PROJECT/$FID".orig" ../data/$PROJECT/$FID".norm" $PROJECT/$FID".fwd" $PROJECT/$FID".fwd+dtw"
	done
done
