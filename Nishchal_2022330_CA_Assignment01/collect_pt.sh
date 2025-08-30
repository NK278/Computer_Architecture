#!/bin/bash
# Script to sweep L2 and L3 configs and collect miss rates (incl. MSHR miss rates)

GEM5=~/gem5/build/RISCV/gem5.opt
SCRIPT=~/gem5/build/RISCV/Nishchal_2022330_CA_Assignment01/two_level.py
BINARY=~/gem5/build/RISCV/Nishchal_2022330_CA_Assignment01/qsort_small.elf
# INPUT=~/gem5/build/RISCV/Nishchal_2022330_CA_Assignment01/input_small.dat

OUTCSV=results.csv
echo "cpu,l2_size,l2_assoc,l3_size,l3_assoc,simTicks,l2_missrate,l3_missrate" > "$OUTCSV"

CPUS=("timing" "o3")

# Table 1 configurations
L2_CONFIGS=("4KiB:2" "4KiB:4" "4KiB:8" "8KiB:2" "8KiB:4" "8KiB:8" "64KiB:2" "64KiB:4" "64KiB:8" "256KiB:2" "256KiB:4" "256KiB:8" "1024KiB:2" "1024KiB:4" "1024KiB:8")
L3_CONFIGS=("1MiB:2" "1MiB:4" "1MiB:8" "1MiB:16" "2MiB:2" "2MiB:4" "2MiB:8" "2MiB:16")

# Helper: get a stat's numeric value by exact key (2nd field), else NA
get_stat() {
  local key="$1"
  local file="$2"
  # stats.txt lines look like: key  value  # comment...
  awk -v K="$key" '($1==K){print $2; found=1; exit} END{if(!found) print "NA"}' "$file"
}

for cpu in "${CPUS[@]}"; do
  for l2 in "${L2_CONFIGS[@]}"; do
    l2_size=${l2%:*}
    l2_assoc=${l2#*:}
    for l3 in "${L3_CONFIGS[@]}"; do
      l3_size=${l3%:*}
      l3_assoc=${l3#*:}

      OUTDIR="m5out_${cpu}_l2${l2_size}a${l2_assoc}_l3${l3_size}a${l3_assoc}"
      echo ">>> Running CPU=$cpu  L2=${l2_size}/${l2_assoc}  L3=${l3_size}/${l3_assoc}"

      mkdir -p "$OUTDIR"

      "$GEM5" "$SCRIPT" \
        --binary="$BINARY"  \
        --cpu="$cpu" \
        --l2_size="$l2_size" --l2_assoc="$l2_assoc" \
        --l3_size="$l3_size" --l3_assoc="$l3_assoc" \
        > "$OUTDIR/run.log" 2>&1

      # Move m5out to unique dir
      if [ -d m5out ]; then
        # If a previous m5out exists in OUTDIR, remove/rename; here we just replace
        rm -rf "$OUTDIR/m5out"
        mv m5out "$OUTDIR/m5out"
      fi

      STATS="$OUTDIR/m5out/stats.txt"
      if [ ! -f "$STATS" ]; then
        echo "No stats.txt for $OUTDIR, skipping..."
        continue
      fi

      # Extract basic stats (fallbacks kept)
      simTicks=$(grep -i -m1 -E '^simTicks|^sim_ticks' "$STATS" | awk '{print $2}')

      
      l2_missrate=$(grep -m1 "system.l2cache.overallMissRate::total" "$STATS" | awk '{print $2}')
      # If your L3 stat exists under this name, we capture it; else it will be NA.
      l3_missrate=$(grep -m1 "system.l3cache.overallMissRate::total" "$STATS" | awk '{print $2}')

      echo "$cpu,$l2_size,$l2_assoc,$l3_size,$l3_assoc,$simTicks,$l2_missrate,$l3_missrate" >> "$OUTCSV"

    done
  done
done

echo "All runs completed. Results saved in $OUTCSV"
