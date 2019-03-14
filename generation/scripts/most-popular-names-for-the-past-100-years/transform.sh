#!/usr/bin/env bash
cat $1/bc-popular-boys-names.csv | cut -d ',' -f 1 >> $1/firstnames.csv.out
cat $1/bc-popular-girls-names.csv | cut -d ',' -f 1 >> $1/firstnames.csv.out