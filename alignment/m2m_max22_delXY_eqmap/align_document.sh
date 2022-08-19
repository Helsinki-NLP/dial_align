#! /bin/bash -l

M2MPATH=../m2m-aligner
DATADIR=../../data

PROJECT=$1
ORIGFILE=$2
FID=`basename $ORIGFILE .orig`

echo "Aligning $PROJECT/$FID (orig file $ORIGFILE)"
paste $DATADIR/$PROJECT/$FID.orig $DATADIR/$PROJECT/$FID.norm > $PROJECT/$FID.input
$M2MPATH/m2m-aligner --inFormat news --sepChar "#" --nullChar "@" --eqMap --delX --delY --errorInFile -i $PROJECT/$FID.input -o $PROJECT/$FID.aligned --alignerOut $PROJECT/$FID.model
python3 ../convert_m2m.py < $PROJECT/$FID.aligned > $PROJECT/$FID.fwd
