# include <iostream>
# include <fstream>
# include <string>
# include <vector>
# include <set>
# include <map>
# include <algorithm>

const int NHEADER = 25;
const std::string input_file = "input";

int find_location(const std::vector<long int> numbers) {
    std::map<std::pair<int, int>, long int> pair2sum;
    std::map<long int, std::set<std::pair<int, int>>> sum2pairs;

    // Loop over lines
    long int sum;
    for (auto i0 = 0; i0 < NHEADER; ++i0) {
        long int v = numbers[i0];
        for (auto j0 = i0 + 1; j0 < NHEADER; ++j0) {
            long int w = numbers[j0];
            sum = v + w;
            pair2sum[{i0, j0}] = sum;
            auto it = sum2pairs.find(sum);
            if (it == sum2pairs.end()) {
                std::set<std::pair<int, int>> new_set({{i0, j0}});
                sum2pairs[sum] = new_set;
            } else
                it->second.insert({i0, j0});
        }
    }
    for (size_t i = NHEADER; i < numbers.size(); ++i) {
        // Early break if no match
        auto it = sum2pairs.find(numbers[i]);
        if (it == sum2pairs.end())
            return i;

        // Proceed to next step: remove old entries...
        size_t i0 = i - NHEADER;
        for (size_t j0 = i0 + 1; j0 < i; ++j0) {
            auto v = pair2sum[{i0, j0}];
            auto it = sum2pairs.find(v);
            auto set = it->second;
            set.erase({i0, j0});
            if (set.size() == 0)
                sum2pairs.erase(v);
            pair2sum.erase({i0, j0});
        }
        // ... and add new ones
        auto j0 = i;
        for (size_t i0 = i - NHEADER; i0 < j0; ++i0) {
            auto sum = numbers[i0] + numbers[j0];
            pair2sum[{i0, j0}] = sum;
            auto it = sum2pairs.find(sum);
            if (it == sum2pairs.end()) {
                std::set<std::pair<int, int>> new_set({{i0, j0}});
                sum2pairs[sum] = new_set;
            } else
                it->second.insert({i0, j0});
        }
    }
    return -1;
}

std::pair<int, int> find_set_boundaries(int istart, int iend, const std::vector<long int> numbers, const long int tgt) {
    // Dynamic programming: first compute the sum of all 2-uples, 3-uples, ...
    std::vector<long int> sums(numbers.size());
    int len = 0;
    while (true) {
        for (auto i = istart; i < iend-len; ++i) {
            sums[i] += numbers[i+len];
            if (sums[i] == tgt) {
                return {i, i+len};
            }
        }
        ++len;
    }
    return {0, 0};
}

int main() {
    std::vector<long int> numbers;
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;
    while(std::getline(myfile, line)){
        numbers.push_back(std::stol(line));
    }
    myfile.close();

    int iout = find_location(numbers);

    std::cout << "numbers["<< iout << "] = " << numbers[iout] << " is not the sum of any two-uple." << std::endl;

    auto ret = find_set_boundaries(0, iout, numbers, numbers[iout]);
    auto minmax = std::minmax_element(numbers.begin() + ret.first, numbers.begin() + ret.second + 1);

    std::cout << "Sum of boundaries that sum to this value is " << *(minmax.first) + *(minmax.second) << "." << std::endl;
}
