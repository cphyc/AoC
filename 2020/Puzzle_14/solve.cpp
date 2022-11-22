# include <fstream>
# include <string>
# include <iostream>
# include <vector>
# include <bitset>
# include <map>
# include <regex>

const std::string input_file = "input";


const std::regex mem_re("mem\\[(\\d*)\\] = (\\d*)");


std::pair<uint64_t, uint64_t> read_mask(const std::string line) {
    std::string smask = line.substr(7, line.size());
    uint64_t X_mask = 0;
    uint64_t mask_value = 0;
    for (auto m: smask) {
        X_mask <<= 1;
        mask_value <<= 1;
        if (m == '0' || m == '1') {
            mask_value |= uint(m - '0');
            X_mask |= 0;
        } else {
            X_mask |= 1;
        }
    }
    return {X_mask, mask_value};
}

std::pair<uint64_t, uint64_t> read_mem(const std::string line) {
    std::smatch m;
    std::regex_match(line, m, mem_re);

    return {std::stoull(m[1].str()), std::stoull(m[2].str())};
}

std::vector<uint64_t> decode_addresses(uint64_t X_mask, uint64_t mask_value, uint64_t imem) {
    std::vector<uint64_t> addrs;
    uint64_t ii = 1;
    imem |= mask_value;
    addrs.push_back(imem);

    for (int ibit = 0; ibit < 36; ++ibit, ii<<=1) {
        if ((X_mask & ii) != 0) {
            size_t len = addrs.size();
            for (size_t i = 0; i < len; ++i)
                addrs.push_back(addrs[i] ^ ii);
        }
    }

    return addrs;
}

void first_part(std::vector<std::string> lines) {
    std::map<uint64_t, uint64_t> memory;
    uint64_t mask, mask_value, mem_value;
    uint64_t imem;
    for (auto line: lines) {
        if (line.substr(0, 4) == "mask") {
            std::tie(mask, mask_value) = read_mask(line);
        } else {
            std::tie(imem, mem_value) = read_mem(line);
            mem_value = (mem_value & mask) | mask_value;
            memory[imem] = mem_value;
        }
    }

    uint64_t sum = 0;
    for (auto const&[key, val]: memory)
        sum += val;

    std::cout << "Part I,  sum = " << sum << std::endl;
}

void second_part(std::vector<std::string> lines) {
    std::map<uint64_t, uint64_t> memory;
    uint64_t mask, mask_value, mem_value;
    uint64_t imem;

    for (auto line: lines) {
        if (line.substr(0, 4) == "mask") {
            std::tie(mask, mask_value) = read_mask(line);
        } else {
            std::tie(imem, mem_value) = read_mem(line);
            auto addrs = decode_addresses(mask, mask_value, imem);
            for (auto imem2: addrs) {
                memory[imem2] = mem_value;
            }
        }
    }

    uint64_t sum = 0;
    for (auto const&[key, val]: memory)
        sum += val;

    std::cout << "Part II, sum = " << sum << std::endl;
}

int main() {
    std::vector<std::string> lines;
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;

    while (std::getline(myfile, line))
        lines.push_back(line);
    myfile.close();

    first_part(lines);

    second_part(lines);
}
