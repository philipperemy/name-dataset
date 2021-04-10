#!/usr/bin/env bash

set -e

export LC_CTYPE=C
OUTPUT_DIR=output

mkdir -p ${OUTPUT_DIR}
rm -rf ${OUTPUT_DIR}

echo "--------------------------------------------------"
echo "Generating the V2 dataset in ${OUTPUT_DIR}/..."
echo "--------------------------------------------------"

ND_PATH="../names_dataset_v2"

python diff_v2.py ${ND_PATH}/last_names.all.csv.original ../eng_dictionary/google-10000-english-no-names.txt ${ND_PATH}/last_names.all.csv
python diff_v2.py ${ND_PATH}/first_names.all.csv.original ../eng_dictionary/google-10000-english-no-names.txt ${ND_PATH}/first_names.all.csv

python diff_v2.py ${ND_PATH}/last_names.all.csv ../eng_dictionary/1000-no-names.txt ${ND_PATH}/last_names.all.csv
python diff_v2.py ${ND_PATH}/first_names.all.csv ../eng_dictionary/1000-no-names.txt ${ND_PATH}/first_names.all.csv


echo "--------------------------------------------------"
echo "Done. Output directory is ${OUTPUT_DIR}/."
echo "${ND_PATH}/last_names.all.csv"
echo "${ND_PATH}/first_names.all.csv"
echo "--------------------------------------------------"

