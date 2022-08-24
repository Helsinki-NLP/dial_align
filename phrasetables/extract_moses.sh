#! /bin/bash

set -e

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

PROJECT=$1
FID=`basename $2 .$4`
DATAFOLDER=../data
ALIGNER=$3
ALIGNFOLDER=../alignment/$3
ALIGN_EXT=$4
PHRASE_LENGTH=$5

echo "  $PROJECT $FID $ALIGNER $ALIGN_EXT $PHRASE_LENGTH"
train-model.perl --first-step 4 --last-step 6 --corpus $DATAFOLDER/$PROJECT/$FID -e norm -f orig --max-phrase-length $PHRASE_LENGTH --alignment-file $ALIGNFOLDER/$PROJECT/$FID --alignment $ALIGN_EXT --extract-file $ALIGNER/$PROJECT/$FID.extract --lexical-file $ALIGNER/$PROJECT/$FID.lex --phrase-translation-table $ALIGNER/$PROJECT/$FID.phrasetable
rm -f $ALIGNER/$PROJECT/$FID.extract.* $ALIGNER/$PROJECT/$FID.lex.*
