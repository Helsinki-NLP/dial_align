# data

We use the following datasets:

## ArchiMob

XML download from here: (https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html)

The file `1244_1.xml` has an XML error, a fixed version is part of this repository.

The phase 1 transcriptions are unified, i.e. the following replacement rules are applied: `à => a`, `ò => o`, `ö̀ => ö`, `ì => e`, `ù => o`, `ǜ = ö`.

## SKN

VRT download from here: (https://metashare.csc.fi/repository/browse/samples-of-spoken-finnish-vrt-version/2da8ae704b9a11eca32afa163ec5ae3ea40636603aeb4aebbee4c394198868d4/)

We extract the simplified transcriptions.

## NDC

Phonetic and orthographic transcriptions available here: (http://www.tekstlab.uio.no/scandiasyn/download.html)

We use the utterance-aligned version available here: (https://github.com/Helsinki-NLP/ndc-aligned)

## Scripts

The scripts perform some preprocessing and write all data to the same format type.
