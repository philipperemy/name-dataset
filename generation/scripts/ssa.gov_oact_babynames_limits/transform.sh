#!/usr/bin/env bash
cat $1/*.txt | cut -d ',' -f 1 > $1/first_names.csv.out
