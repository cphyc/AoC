#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <map>

const std::string input_file = "input_example";

int read_block(std::fstream &fd, std::map<int, std::vector<std::vector<int>>> &blocks) {
    std::string line;
    std::vector<std::vector<int>> block_content;

    if (!std::getline(fd, line))
        return 1;

    int iblock = std::stoi(line.substr(5, line.size()-6));

    while (std::getline(fd, line) && line != "") {
        std::vector<int> block_line = {};
        for (char c: line)
            block_line.push_back((c == '#') ? 1 : 0);
        block_content.push_back(block_line);
    }
    blocks[iblock] = block_content;
    return 0;
}

typedef std::vector<std::vector<int>> block_t;

std::vector<std::vector<int>> align_blocks(block_t b1, block_t b2, int iblock1, int iblock2) {
    // Find common corners
    int N = b1.size()-1;
    auto extract_i = [=](block_t b, int j) {
        std::vector<int> ret;
        for (auto i = 0; i < N; ++i)
            ret.push_back(b[i][j]);
        return ret;
    };
    auto extract_j = [=](block_t b, int i) {
        std::vector<int> ret;
        for (auto j = 0; j < N; ++j)
            ret.push_back(b[i][j]);
        return ret;
    };
    std::vector<std::vector<int>> lines1 = {
        extract_i(b1, 0),
        extract_j(b1, N),
        extract_i(b1, N),
        extract_j(b1, 0),
    };
    std::vector<std::vector<int>> lines2 = {
        extract_i(b2, 0),
        extract_j(b2, N),
        extract_i(b2, N),
        extract_j(b2, 0),
    };

    std::vector<std::vector<int>> candidates;
    for (auto i = 0; i < 4; ++i) {
        auto l1 = lines1[i];
        for (auto j = 0; j < 4; ++j) {
            auto l2 = lines2[j];
            if (std::equal(l1.cbegin(), l1.cend(), l2.cbegin(), l2.cend()))
                candidates.push_back({iblock1, iblock2, i, j, +1});
            if (std::equal(l1.cbegin(), l1.cend(), l2.crbegin(), l2.crend()))
                candidates.push_back({iblock1, iblock2, i, j, -1});
        }
    }
    // std::cout << "FOUND " << candidates.size() << " match" << std::endl;
    return candidates;
}

void part_I(std::map<int, block_t> &blocks) {
    std::vector<std::vector<int>> matings;
    std::vector<int> Nneigh(blocks.size(), 0);
    std::vector<int[4]> neighbours(blocks.size());

    // Now we need to mate blocks
    int i = 0;
    for (auto const& [id1, b1]: blocks) {
        int j = 0;
        for (auto const& [id2, b2]: blocks) {
            if (id1 <= id2) continue;
            auto tmp = align_blocks(b1, b2, id1, id2);
            for (auto r: tmp)
                matings.push_back(r);
            Nneigh[i] += 1;
            Nneigh[j] += 1;
            ++j;
        }
        ++i;
    }
    std::cout << "Found " << matings.size() << " matings." << std::endl;
    int N = 1;
    while (N*N != blocks.size()) ++N;
    std::pair<int, int> placement[N][N];
    for (auto m: mattings)
}

int main() {
    std::vector<std::string> lines;
    std::fstream myfile(input_file, std::ios_base::in);
    std::map<int, block_t> blocks;

    int stop = 0;

    while (!stop) {
        stop = read_block(myfile, blocks);
    }
    myfile.close();

    part_I(blocks);
    // for (auto it1: blocks.begin(); it1 < blocks.end(); ++it1) {
    //     for (auto it2: it1; it2 < blocks.end(); ++it2) {
    //         // Try all combinations

    //     }
    // }
}
