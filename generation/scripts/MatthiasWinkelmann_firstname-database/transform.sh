#!/usr/bin/env bash
cat $1/firstnames.csv | cut -d ';' -f 1  > $1/firstnames.csv.out
