#!/usr/bin/env bash
cat $1/* | cut -d ',' -f 2 > $1/first_names.csv.out
