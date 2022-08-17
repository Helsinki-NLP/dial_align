#! /bin/bash

mkdir -p archimob-gold
cd archimob-gold
for ID in 1007 1048 1063 1143 1198 1270; do
	ln -s ../archimob/$ID.orig $ID.orig
	ln -s ../archimob/$ID.norm $ID.norm
done
