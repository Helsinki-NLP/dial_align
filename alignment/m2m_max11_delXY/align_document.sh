#! /bin/bash -l

M2MPATH=../m2m-aligner
DATADIR=../../data

PROJECT=$1
ORIGFILE=$2
FID=`basename $ORIGFILE .orig`

echo "Aligning $PROJECT/$FID (orig file $ORIGFILE)"
paste $DATADIR/$PROJECT/$FID.orig $DATADIR/$PROJECT/$FID.norm > $PROJECT/$FID.input
$M2MPATH/m2m-aligner --inFormat news --sepChar "#" --nullChar "@" --delX --delY --maxX 1 --maxY 1 --errorInFile -i $PROJECT/$FID.input -o $PROJECT/$FID.aligned --alignerOut $PROJECT/$FID.model
python3 ../convert_m2m.py < $PROJECT/$FID.aligned > $PROJECT/$FID.fwd
python3 ../add_adjacent_identicals.py $DATADIR/$PROJECT/$FID".orig" $DATADIR/$PROJECT/$FID".norm" $PROJECT/$FID".fwd" $PROJECT/$FID".fwd+aai"
#rm $PROJECT/$FID.input $PROJECT/$FID.aligned $PROJECT/$FID.aligned.err $PROJECT/$FID.model
