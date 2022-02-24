#!/bin/bash
rm out.txt
for f in input_data/*.txt; do 
  echo "Running on $f";
  name=$(basename "$f")
  ./a < "input_data/$name" > "out/$name"
done