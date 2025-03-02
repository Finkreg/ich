#!/bin/bash
#
# a short loop that generates 100 files for a linux homework
for i in {1..100}
do
	random_num=$RANDOM
	touch Dir1/"$random_num.txt"
done
