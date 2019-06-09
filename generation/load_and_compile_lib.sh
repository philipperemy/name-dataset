#!/usr/bin/env bash

cp output/first_names.all.txt ../names_dataset/
cp output/last_names.all.txt ../names_dataset/

cd ..

pip install . --upgrade
pip install scikit-learn

python evaluate.py english_common_words/1000.txt
python evaluate.py english_common_words/google-10000-english.txt
