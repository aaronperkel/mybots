#!/usr/bin/env bash
set -e

# how many replicates each
REPS=50

# output CSV (in project root)
OUT=fitness_ab_test.csv
echo "method,replica,fitness" > $OUT

for method in max avg; do
  export FITNESS_METHOD=$method
  for i in $(seq 1 $REPS); do

    # run the GA (this launches simulate.py in the background)
    python src/search.py

    # wait for whichever fitness_<method><ID>.txt shows up
    # (Show_Best writes fitness_max<ID>.txt or fitness_avg<ID>.txt)
    file=""
    until file=$(ls src/data/fitness_${method}*.txt 2>/dev/null | head -n1); do
      sleep 0.1
    done

    FIT=$(cat "$file")
    echo "${method},${i},${FIT}" >> $OUT
    echo "  [${method} run $i → $FIT]"
  done
done

echo "done → results in $OUT"