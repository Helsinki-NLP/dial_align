#! /bin/bash -l

EXP=$1
EXT=$2

echo $EXP $EXT

CURPWD=$PWD
mkdir -p $EXP/archimob-gold
cd $EXP/archimob-gold
for ID in 1007 1048 1063 1143 1198 1270; do
	if [ ! -f $ID.$EXT ]; then
		ln -s ../archimob/$ID.$EXT $ID.$EXT
	fi
done
cd $CURPWD

touch $EXP/eval.$EXT.txt
echo "" > $EXP/eval.$EXT.txt
for PROJ in archimob archimob-gold ndc skn; do
	python3 evaluate.py "$EXP/$PROJ/*.$EXT" ../data >> $EXP/eval.$EXT.txt
done
