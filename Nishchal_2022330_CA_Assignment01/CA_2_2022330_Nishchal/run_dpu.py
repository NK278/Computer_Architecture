# configs/learning_gem5/part2/run_dataproc.py

from m5.objects import *
import m5

# Create system object
system = System()

# Attach a clock and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Instantiate your DataProcessingUnit
system.dpu = DataProcessingUnit()

# Root is the top-level container
root = Root(full_system=False, system=system)

# Instantiate and run
m5.instantiate()
print("Beginning simulation with DataProcessingUnit...")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))

