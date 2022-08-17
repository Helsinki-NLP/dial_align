#! /bin/bash -l

M2MPATH=../m2m/m2m-aligner

PROJECT=$1
ORIGFILE=$2
FID=`basename $ORIGFILE .orig`

echo "Aligning $PROJECT/$FID (orig file $ORIGFILE)"
paste ../data/$PROJECT/$FID.orig ../data/$PROJECT/$FID.norm > $PROJECT/$FID.input
$M2MPATH/m2m-aligner --inFormat news --sepChar "#" --nullChar "@" --errorInFile -i $PROJECT/$FID.input -o $PROJECT/$FID.aligned --alignerOut $PROJECT/$FID.model
python3 convert.py < $PROJECT/$FID.aligned > $PROJECT/$FID.fwd
#rm $PROJECT/$FID.input $PROJECT/$FID.aligned $PROJECT/$FID.aligned.err $PROJECT/$FID.model
