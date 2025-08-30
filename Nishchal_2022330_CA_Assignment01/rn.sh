#!/bin/bash
# Script to run gem5 with given configuration and binary

# Path to gem5 executable
GEM5=~/gem5/build/RISCV/gem5.opt

# Path to your config file
SCRIPT=~/gem5/build/RISCV/Nishchal_2022330_CA_Assignment01/two_level.py

# Binary to run
BINARY=~/gem5/build/RISCV/Nishchal_2022330_CA_Assignment01/qsort_small.elf

# CPU type
CPU=o3

# Run gem5
$GEM5 $SCRIPT \
  --binary=$BINARY \
  --cpu=$CPU
