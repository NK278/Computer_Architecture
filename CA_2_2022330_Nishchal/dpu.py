from m5.params import *
from m5.SimObject import SimObject

class DataProcessingUnit(SimObject):
    type = 'DataProcessingUnit'
    cxx_header = "learning_gem5/part2/dpu.hh"
    cxx_class = "gem5::DataProcessingUnit"

