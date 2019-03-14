#!/usr/bin/env bash
awk '{gsub(/\"/,"")};1' $1/baby-names.csv | cut -d ',' -f 2 > $1/first_names.csv.out
