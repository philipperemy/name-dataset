#!/usr/bin/env bash

# GENERATE STATS.

INPUT_DIR="/Users/premy/Downloads/curate"
TMP_DIR="/tmp/generate"
TMP_DIR2="/tmp/generate2"
MAX_NAMES="1000"
DEBUG="--debug"
#DEBUG=""

rm -rf ${TMP_DIR} ${TMP_DIR2}

# one by one because it's too memory intensive.
for option in "first_by_country" "last_by_country" "country_by_first" "country_by_last" "gender_by_first"
do
  python generate_stats.py --input_dir ${INPUT_DIR} \
                           --output_dir ${TMP_DIR} \
                           --option ${option} \
                           ${DEBUG}
done

# FILTER NAMES.
python filter_records.py --input_dir ${TMP_DIR} \
                         --output_dir ${TMP_DIR2} \
                         --trunc_first_names_count ${MAX_NAMES} \
                         --trunc_last_names_count ${MAX_NAMES}