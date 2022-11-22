# include <vector>
# include <fstream>
# include <string>
# include <algorithm>
# include <map>
# include <iostream>
# include <set>

const std::string input_file = "input";

std::tuple<int, int, int> count_n_jolts(const std::vector<int> numbers) {
    int v1, v2, i = 0;
    std::map<int, int> counts;
    counts[numbers[0]] = 1; // diff to input
    counts[3] = 1;          // diff to device is always 3
    for (auto it = numbers.begin(); it < numbers.end()-1; ++it, ++i) {
        v1 = *it;
        v2 = *(it + 1);
        auto p = counts.find(v2-v1);
        if (v2 - v1 > 3)
            throw "Cannot find a common rating";

        if (p == counts.end())
            counts[v2-v1] = 1;
        else
            ++p->second;
    }

    // Print the number of counts
    for (auto const& [diff, count]: counts)
        std::cout << "Counted " << count << " times a difference of " << diff << " jolt(s)" << std::endl;
    std::cout << "#1-jolt x #3-jolts = " << counts[1] * counts[3] << std::endl;

    return {counts[1], counts[2], counts[3]};
}

void find_arrangements(const std::vector<int> numbers) {
    // Loop over (ordered) numbers, whenever the difference is 3, try to skip it
    std::set<int> possible_next = {0};
    const std::set<int> number_set(numbers.begin(), numbers.end());

    // All numbers can be reached with the base combination
    int N = numbers.size();
    std::vector<int64_t> comb(N);
    comb[N-1] = 1;

    for (int k = N - 2; k >= 0; --k)
        for (int i = k + 1; i < N && numbers[i] - numbers[k] <= 3; ++i)
            comb[k] += comb[i];

    std::cout << "Ncombinations: " << comb[0] << std::endl;
}


int main() {
    std::vector<int> numbers;
    numbers.push_back(0);
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;
    while(std::getline(myfile, line)){
        numbers.push_back(std::stoi(line));
    }
    myfile.close();

    // Sort the inputs
    std::sort(numbers.begin(), numbers.end());

    int n1, n2, n3;
    std::tie(n1, n2, n3) = count_n_jolts(numbers);
    find_arrangements(numbers);

}
