# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""This file creates a single CPU and a two-level cache system.
This script takes a single parameter which specifies a binary to execute.
If none is provided it executes 'hello' by default (mostly used for testing)
"""

# import the m5 (gem5) library created when gem5 is built
import m5

# import all of the SimObjects
from m5.objects import *

# Add the common scripts to our path
m5.util.addToPath("/home/monsoon2025/nishchal22330/gem5/configs")

# import the caches which we made
from caches import *
# import caches as ch
# import caches as myc

# import the SimpleOpts module
from common import SimpleOpts

# Default to running 'hello', use the compiled ISA to find the binary
# grab the specific path to the binary
thispath = os.path.dirname(os.path.realpath(__file__))
# default_binary = "/home/monsoon2025/nishchal22330/gem5/qsort_small.elf"
SimpleOpts.add_option(
    "--binary",
    help="Path to a RISC-V ELF binary to run (e.g., qsort_small.elf)",
    default=None,
)

SimpleOpts.add_option(
    "--cpu",
    help="CPU model: 'timing' (RiscvTimingSimpleCPU) or 'o3' (RiscvO3CPU). Default: timing",
    default="timing",
)

SimpleOpts.add_option("--l2_assoc", help="L2 associativity", default="4")
SimpleOpts.add_option("--l3_size",  help="L3 size (e.g., 1MiB, 2MiB)", default="1MiB")
SimpleOpts.add_option("--l3_assoc", help="L3 associativity",           default="8")

# SimpleOpts.add_option(
#     "--l1d_size",
#     help="Override L1 data cache size. Assignment default: 16KiB",
#     default="16KiB",
# )



# Binary to execute
# SimpleOpts.add_option("binary", nargs="?", default=default_binary)
# Finalize the arguments and grab the args so we can pass it on to our objects
args = SimpleOpts.parse_args()
if not args.binary:
    raise RuntimeError("Please provide --binary=/full/path/to/qsort_small.elf (RISC-V ELF)")


# create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Memory system
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

# CPU model RiscvTimingSimpleCPU() and RiscvO3CPU()
cpu_kind=(args.cpu or "timing").lower()
if cpu_kind=="o3": system.cpu=RiscvO3CPU()
elif cpu_kind=="timing": system.cpu=RiscvTimingSimpleCPU()
else: raise RuntimeError(" use only 'timing' or 'o3' " )

if not getattr(args,'l1d_size',None): args.l1d_size="16KiB"

#   L1
system.cpu.icache=L1ICache(args)
system.cpu.dcache=L1DCache(args)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Buses
system.l2bus=L2XBar() # between L1 and L2
system.l3bus=L2XBar() # between L2 and L3
system.membus=SystemXBar() # below L3 to memory ctrl

# L1s to L2 bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# L2
system.l2cache=L2Cache(args)
if not getattr(args, "l2_size", None):
    system.l2cache.size = "512KiB"     # enforce assignment default
# system.l2cache.size="512KiB"
system.l2cache.assoc=int(args.l2_assoc)
system.l2cache.tag_latency=10
system.l2cache.data_latency=10
system.l2cache.response_latency=10
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.l3bus)

# L3
system.l3cache=L2Cache()
# system.l3cache.size="1MiB"
system.l3cache.size  = args.l3_size
# system.l3cache.assoc=8
system.l3cache.assoc = int(args.l3_assoc)
system.l3cache.connectCPUSideBus(system.l3bus)
system.l3cache.connectMemSideBus(system.membus)
#  for o3
# create the interrupt controller for the CPU
system.cpu.createInterruptController()
# system.cpu.interrupts[0].pio           = system.membus.mem_side_ports
# system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
# system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# System port & memory
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(args.binary)

# creating process
proc = Process()
proc.cmd = [args.binary,'/home/monsoon2025/nishchal22330/gem5/build/RISCV/Nishchal_2022330_CA_Assignment01/input_small.dat']
system.cpu.workload = proc
system.cpu.createThreads()

# Running

root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")


