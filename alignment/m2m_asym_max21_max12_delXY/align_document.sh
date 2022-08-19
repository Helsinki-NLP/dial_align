#! /bin/bash -l

M2MPATH=../m2m-aligner
DATADIR=../../data

PROJECT=$1
ORIGFILE=$2
FID=`basename $ORIGFILE .orig`

echo "Aligning $PROJECT/$FID (orig file $ORIGFILE)"
paste $DATADIR/$PROJECT/$FID.orig $DATADIR/$PROJECT/$FID.norm > $PROJECT/$FID.input
$M2MPATH/m2m-aligner --inFormat news --maxX 2 --maxY 1 --delX --delY --sepChar "#" --nullChar "@" --errorInFile -i $PROJECT/$FID.input -o $PROJECT/$FID.fwd.aligned --alignerOut $PROJECT/$FID.fwd.model
$M2MPATH/m2m-aligner --inFormat news --maxX 1 --maxY 2 --delX --delY --sepChar "#" --nullChar "@" --errorInFile -i $PROJECT/$FID.input -o $PROJECT/$FID.rev.aligned --alignerOut $PROJECT/$FID.rev.model

python3 ../convert_m2m.py < $PROJECT/$FID.fwd.aligned > $PROJECT/$FID.fwd
python3 ../convert_m2m.py < $PROJECT/$FID.rev.aligned > $PROJECT/$FID.rev

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

atools -c grow-diag-final-and -i$PROJECT/$FID".fwd" -j$PROJECT/$FID".rev" > $PROJECT/$FID".sym"
