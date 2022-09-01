#! /bin/bash -l

module load python-data

ALIGNER=eflomal
THRESHOLD=0.05

for FEAT in au ck ei ll nn u hat_; do
	echo $ALIGNER archimob $FEAT
	python3 extractSingleFeature.py $ALIGNER archimob $FEAT $THRESHOLD
done

for FEAT in bl; do
	echo $ALIGNER ndc $FEAT
	python3 extractSingleFeature.py $ALIGNER ndc $FEAT $THRESHOLD
done

for FEAT in ai oi ie uo yö d; do
	echo $ALIGNER skn $FEAT
	python3 extractSingleFeature.py $ALIGNER skn $FEAT $THRESHOLD
done

python3 extractFeatureSet.py eflomal archimob 0.05 u i ü
python3 extractFeatureSet.py eflomal skn 0.05 uo ie yö
