set -e

find . -name "*.out" -type f -delete

for dir in */; do
  echo "$dir"
  cd $dir
  ./transform.sh
  cd ..
done
