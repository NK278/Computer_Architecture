#ifndef __LEARNING_GEM5_PART2_DATA_PROCESSING_UNIT_HH__
#define __LEARNING_GEM5_PART2_DATA_PROCESSING_UNIT_HH__

#include <string>
#include <vector>

#include "params/DataProcessingUnit.hh"
#include "sim/sim_object.hh"
#include "sim/eventq.hh"   // ✅ Correct include for EventFunctionWrapper

namespace gem5
{

class DataProcessingUnit : public SimObject
{
  public:
    using Params = DataProcessingUnitParams;

    DataProcessingUnit(const Params &p);

    /** Called at simulation startup to schedule events */
    void startup() override;

  private:
    /** Task methods */
    void StringReversal();
    void FactorialComputation();
    void ArraySorting();

    /** Input data */
    std::string input_str;
    int fact_num;
    std::vector<int> arr;

    /** Events for tasks */
    EventFunctionWrapper event;   // String reversal
    EventFunctionWrapper event1;  // Factorial computation
    EventFunctionWrapper event2;  // Array sorting
};

} // namespace gem5

#endif // __LEARNING_GEM5_PART2_DATA_PROCESSING_UNIT_HH__

