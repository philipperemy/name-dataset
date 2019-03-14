#!/usr/bin/env bash
# cat name.basics.tsv | grep -E "actor|actress" | cut -d$'\t' -f 2 | cut -d ' ' -f 1 > first_names.csv.out
#cat name.basics.tsv | grep -E "actor|actress" | cut -d$'\t' -f 2 | cut -d ' ' -f 2 > last_names.csv.out

# cat name.basics.tsv | awk -F"\t" '{print $2}' | grep " " | cut -d ' ' -f 1 > first_names.csv.out
# cat name.basics.tsv | awk -F"\t" '{print $2}' | grep " " | cut -d ' ' -f 2 > last_names.csv.out
# sort last_names.csv.out | uniq -c | sort -bgr > out
# cat out | grep -v '   3' | grep -v '   2' | grep -v '   1' | grep -v '   4' | awk '{$1=$1};1' | cut -d' ' -f 2 | grep -E "^[A-Za-z]+$" > last_names.csv.out

echo "Please be patient on this one..."

cat $1/name.basics.tsv | awk -F"\t" '{print $2}' | grep " " | cut -d ' ' -f 2 | sort | uniq -c | sort -bgr | grep -v '   3 ' | grep -v '   2 ' | grep -v '   1 ' | grep -v '   4 ' | awk '{$1=$1};1' | cut -d' ' -f 2 | grep -E "^[A-Za-z]+$" > $1/last_names.csv.out
cat $1/name.basics.tsv | awk -F"\t" '{print $2}' | grep " " | cut -d ' ' -f 1 | sort | uniq -c | sort -bgr | grep -v '   3 ' | grep -v '   2 ' | grep -v '   1 ' | grep -v '   4 ' | awk '{$1=$1};1' | cut -d' ' -f 2 | grep -E "^[A-Za-z]+$" > $1/first_names.csv.out

