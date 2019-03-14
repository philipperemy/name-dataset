#!/usr/bin/env bash
#cp $1/CSV_Database_of_First_Names.csv $1/CSV_Database_of_First_Names.csv.out
#cp $1/CSV_Database_of_Last_Names.csv $1/CSV_Database_of_Last_Names.csv.out

python $(pwd)/transform.py $1/CSV_Database_of_Last_Names.csv
python $(pwd)/transform.py $1/CSV_Database_of_First_Names.csv
