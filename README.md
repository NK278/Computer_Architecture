# Computer_Architecture

Explorations in computer architecture through cycle-accurate simulation (gem5) and upcoming FPGA prototyping (Vivado). The repository captures experiments, insights, and artifacts produced while studying how microarchitectural choices impact performance, power, and efficiency.

## Focus & Scope

- **Instruction Set & Microarchitecture**  
  Single-cycle vs. pipelined cores, hazards, forwarding, and basic out-of-order ideas.

- **Memory System**  
  Cache hierarchies (L1/L2/L3), associativity, line size, MSHRs, replacement and write policies, prefetchers, and DRAM timing effects.

- **Branch Prediction**  
  Static vs. dynamic predictors, BTBs/RAS, and misprediction costs.

- **Multiprocessing & Coherence (planned)**  
  MESI/MOESI protocols, directory vs. snooping, interconnect topologies, and contention.

- **FPGA Prototyping (planned)**  
  RTL experimentation for components like cache controllers, simple pipelines, and AXI-based memory interfaces.

## Tools

- **gem5** — Primary simulator for running controlled microarchitecture experiments and collecting stats.  
- **Xilinx Vivado (planned)** — For synthesizing/implementing RTL prototypes on FPGA to validate ideas in hardware.

## Learning Objectives

- Build intuition for how architectural parameters trade off throughput, latency, and energy.
- Design experiments, gather gem5 statistics, and interpret results rigorously.
- Translate selected architectural blocks into RTL and evaluate them on FPGA.

## Acknowledgements

- [gem5](https://www.gem5.org/) — open-source computer architecture simulator.  
- Xilinx **Vivado** — FPGA design suite used for prototyping.

---

> This repository prioritizes **concepts and experiments** in computer architecture. Setup notes and scripts may appear over time, but the central goal is to document what is learned about architectural design decisions and their real performance impact.
