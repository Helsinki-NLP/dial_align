#! /bin/bash

FOLDER=$1
EXT=$2

mkdir -p $FOLDER/archimob-gold
cd $FOLDER/archimob-gold
for ID in 1007 1048 1063 1143 1198 1270; do
	ln -s ../archimob/$ID.$EXT $ID.$EXT
done

