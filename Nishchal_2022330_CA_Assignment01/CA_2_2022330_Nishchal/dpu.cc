#include "learning_gem5/part2/dpu.hh"
#include "base/trace.hh"
#include "debug/REVSTRING.hh"
#include "debug/FACTORIALRESULT.hh"
#include "debug/SORTRESULT.hh"
#include "sim/sim_exit.hh"
#include <iostream>
#include <algorithm>

namespace gem5
{

// Global/static variables for user inputs
std::string input_str;
int fact_num;
std::vector<int> arr;

DataProcessingUnit::DataProcessingUnit(const DataProcessingUnitParams &p)
    : SimObject(p),
      event([this]{ StringReversal(); }, name() + ".event"),
      event1([this]{ FactorialComputation(); }, name() + ".event1"),
      event2([this]{ ArraySorting(); }, name() + ".event2")
{
    // --- Take user input here ---
    std::cout << "Enter a string for reversal: ";
    std::cin >> input_str;

    std::cout << "Enter a number for factorial: ";
    std::cin >> fact_num;
    if (fact_num < 0) fact_num = 0;

    int n;
    std::cout << "Enter number of elements for sorting: ";
    std::cin >> n;
    arr.resize(n);

    std::cout << "Enter " << n << " integers: ";
    for (int i = 0; i < n; i++) {
        std::cin >> arr[i];
    }

    // Debug prints for confirmation
    DPRINTF(FACTORIALRESULT, "User provided factorial number: %d\n", fact_num);

    std::string arr_str = "User provided array: ";
    for (auto v : arr) arr_str += std::to_string(v) + " ";
    DPRINTF(SORTRESULT, "%s\n", arr_str.c_str());
}

void
DataProcessingUnit::startup()
{
    int tick_str, tick_fact, tick_sort;

    std::cout << "Enter tick for String Reversal: ";
    std::cin >> tick_str;

    std::cout << "Enter tick for Factorial: ";
    std::cin >> tick_fact;

    std::cout << "Enter tick for Sorting: ";
    std::cin >> tick_sort;

    if (tick_str < 0 || tick_fact < 0 || tick_sort < 0) {
        tick_str = 100;
        tick_fact = 1000;
        tick_sort = 10000;
    }

    schedule(event, tick_str);
    schedule(event1, tick_fact);
    schedule(event2, tick_sort);
}

void
DataProcessingUnit::StringReversal()
{
    std::string reversed(input_str.rbegin(), input_str.rend());
    // Print in a single DPRINTF call
    std::string output = "Original: " + input_str + ", Reversed: " + reversed;
    DPRINTF(REVSTRING, "%s\n", output.c_str());
}

void
DataProcessingUnit::FactorialComputation()
{
    long long result = 1;
    for (int i = 1; i <= fact_num; i++) {
        result *= i;
    }
    // Print in a single DPRINTF call
    std::string output = "Factorial of " + std::to_string(fact_num) + " is " + std::to_string(result);
    DPRINTF(FACTORIALRESULT, "%s\n", output.c_str());
}

void
DataProcessingUnit::ArraySorting()
{
    std::vector<int> sorted = arr;
    std::sort(sorted.begin(), sorted.end());

    // Build the output string first
    std::string output = "Sorted array: ";
    for (auto v : sorted) {
        output += std::to_string(v) + " ";
    }

    // Print once with DPRINTF
    DPRINTF(SORTRESULT, "%s\n", output.c_str());

    exitSimLoop("Completed DataProcessingUnit tasks");
}

} // namespace gem5

