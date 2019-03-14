#!/usr/bin/env bash
cat $1/dist.all.last | cut -d ' ' -f 1 > $1/last_names.csv.out
