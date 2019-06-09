#!/usr/bin/env bash

set -e

export LC_CTYPE=C
OUTPUT_DIR=output

mkdir -p ${OUTPUT_DIR}
rm -rf ${OUTPUT_DIR}

echo "--------------------------------------------------"
echo "Generating the whole dataset in ${OUTPUT_DIR}/..."
echo "It takes around 7min on a MacBookPro 2017."
echo "--------------------------------------------------"

DATASET=MatthiasWinkelmann_firstname-database
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://github.com/MatthiasWinkelmann/firstname-database/raw/master/firstnames.csv -P ${OUTPUT_DIR}/${DATASET}/
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

#DATASET=cs.cmu.edu.ai-repository
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/female.txt -P ${OUTPUT_DIR}/${DATASET}
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/male.txt -P ${OUTPUT_DIR}/${DATASET}
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/other/family.txt -P ${OUTPUT_DIR}/${DATASET}
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/other/names.txt -P ${OUTPUT_DIR}/${DATASET}
#bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=yorkshiretwist
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/yorkshiretwist/WTester/master/WTester/Helpers/CSV_Database_of_First_Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/yorkshiretwist/WTester/master/WTester/Helpers/CSV_Database_of_Last_Names.csv -P ${OUTPUT_DIR}/${DATASET}

python scripts/${DATASET}/transform.py ${OUTPUT_DIR}/${DATASET}/CSV_Database_of_First_Names.csv
python scripts/${DATASET}/transform.py ${OUTPUT_DIR}/${DATASET}/CSV_Database_of_Last_Names.csv

DATASET=github_hadley_data-baby-names
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

#DATASET=datasets_imdb
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://datasets.imdbws.com/name.basics.tsv.gz -P ${OUTPUT_DIR}/${DATASET}
#gunzip ${OUTPUT_DIR}/${DATASET}/*
#bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=github_com_dominictarr_random-name
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/dominictarr/random-name/master/names.txt -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=github_com_dominictarr_random-name
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/first%20names/non-normalized/es.txt -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/


DATASET=httpswwwsajaricompublic-data
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.sajari.com/free-data/CSV_Database_of_First_Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.sajari.com/free-data/CSV_Database_of_Last_Names.csv -P ${OUTPUT_DIR}/${DATASET}
python scripts/${DATASET}/transform.py ${OUTPUT_DIR}/${DATASET}/CSV_Database_of_First_Names.csv
python scripts/${DATASET}/transform.py ${OUTPUT_DIR}/${DATASET}/CSV_Database_of_Last_Names.csv

DATASET=mbejda.github.io
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/1e77ee4ad268916142a6/raw/22d1b475217be7240aba54c1a1b545557d624ba8/Hispanic-Female-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/21fbbfe24efd2a114800/raw/52db651f79a716c87b21ef06c224ff443cb41f06/Hispanic-Male-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/26ad0574eda7fca78573/raw/6936d1a8f5fa5220f2f60a51a06a35b172c50f93/White-Female-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/61eb488cec271086632d/raw/6340b8045b28c2abc0b1d44cfbc80f40284ef890/Black-Male-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/6c2293ba3333b7e76269/raw/60aa0c95e8ee9b11b915a26f47480fef5c3203ed/White-Male-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/7f86ca901fe41bc14a63/raw/38adb475c14a3f44df9999c1541f3a72f472b30d/Indian-Male-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/9b93c7545c9dd93060bd/raw/b582593330765df3ccaae6f641f8cddc16f1e879/Indian-Female-Names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://gist.githubusercontent.com/mbejda/9dc89056005a689a6456/raw/bb6ef2375f1289d0ef10dbd8e9469670ac23ceab/Black-Female-Names.csv -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=most-popular-names-for-the-past-100-years
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://catalogue.data.gov.bc.ca/dataset/bfcdd4d7-056b-4069-a09e-5dbda4d11841/resource/2d8c478f-3223-4883-a300-1cac7a344ee3/download/bc-popular-boys-names.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://catalogue.data.gov.bc.ca/dataset/db803d65-bcfa-44e8-b98d-76e7b02f3500/resource/c9a3af38-f374-412a-9cbe-0dd590f677f9/download/bc-popular-girls-names.csv -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=OpenGenderTracking_globalnamedata
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://github.com/OpenGenderTracking/globalnamedata/raw/master/assets/uknames.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://github.com/OpenGenderTracking/globalnamedata/raw/master/assets/ukprocessed.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://github.com/OpenGenderTracking/globalnamedata/raw/master/assets/usnames.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://github.com/OpenGenderTracking/globalnamedata/raw/master/assets/usprocessed.csv -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=ssa.gov_oact_babynames_limits
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.ssa.gov/oact/babynames/names.zip -P ${OUTPUT_DIR}/${DATASET}
unzip ${OUTPUT_DIR}/${DATASET}/* -d ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=www.nrscotland.gov.uk
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-17-historical-16.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-17-historical-17.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-2010.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-2011.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-2012.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-2013.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-2014.csv -P ${OUTPUT_DIR}/${DATASET}
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www.nrscotland.gov.uk/files//statistics/babies-first-names-full-list/2010-2019/babies-first-names-2015.csv -P ${OUTPUT_DIR}/${DATASET}
export LC_ALL=C; bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

DATASET=www2.census.gov.1990surnames
wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://www2.census.gov/topics/genealogy/1990surnames/dist.all.last -P ${OUTPUT_DIR}/${DATASET}
bash scripts/${DATASET}/transform.sh ${OUTPUT_DIR}/${DATASET}/

#wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/first%20names/all.txt -P ${OUTPUT_DIR}/${DATASET}
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/first%20names/us.txt -P ${OUTPUT_DIR}/${DATASET}
#wget -nv --read-timeout=30 --tries=3 --waitretry=5 https://static1.squarespace.com/static/588c1f531e5b6c553fe26beb/t/59e8fd7d017db27f7ad2ef7a/1508441525530/F104B59A-C180-4DD1-982B-99A536ACA55F.jpeg-P ${OUTPUT_DIR}/${DATASET}

echo "Generating the first and last names files"
export LC_CTYPE=C; find ${OUTPUT_DIR} -name '*irst*.out' -print0 | xargs -0 cat | awk '{print tolower($0)}' | awk '{$1=$1};1' | grep -v '@' | grep -v '"' | grep -v '\.' | grep -v '+' | grep -v ' ' | sort | uniq > ${OUTPUT_DIR}/first_names.all.txt
export LC_CTYPE=C; find ${OUTPUT_DIR} -name '*last*.out' -print0 | xargs -0 cat | awk '{print tolower($0)}' | awk '{$1=$1};1' | grep -v '@' | grep -v '"' | grep -v '\.' | grep -v '+' | grep -v ' ' | sort | uniq > ${OUTPUT_DIR}/last_names.all.txt

python diff.py ${OUTPUT_DIR}/last_names.all.txt ../eng_dictionary/google-10000-english-no-names.txt ${OUTPUT_DIR}/last_names.all.txt -
python diff.py ${OUTPUT_DIR}/first_names.all.txt ../eng_dictionary/google-10000-english-no-names.txt ${OUTPUT_DIR}/first_names.all.txt -

echo "--------------------------------------------------"
echo "Done. Output directory is ${OUTPUT_DIR}/."
echo "> find ${OUTPUT_DIR} | grep '.out' to find the aux files."
echo " First names: ${OUTPUT_DIR}/first_names.all.txt."
echo " Last names: ${OUTPUT_DIR}/last_names.all.txt."
echo "--------------------------------------------------"

