# include <vector>
# include <fstream>
# include <string>
# include <algorithm>
# include <map>
# include <iostream>
# include <set>

const std::string input_file = "input";

const uint8_t FLOOR=2, EMPTY=0, OCCUPIED=1;

/********************************************************************
 * Helper functions
 * */
inline int ijk (int i, int j, int M) {
    return i*M + j;
}
inline std::pair<int, int> jki(int ijk, int M) {
    return {ijk / M, ijk % M};
}

void print_map(std::vector<uint8_t> map, const int N, const int M) {
    std::cout << "----------------------------------" << std::endl;
    for (auto i = 0; i < N; ++i) {
        for (auto j = 0; j < M; ++j) {
            if (map[ijk(i, j, M)] == OCCUPIED)
                std::cout << "#";
            if (map[ijk(i, j, M)] == EMPTY)
                std::cout << "L";
            if (map[ijk(i, j, M)] == FLOOR)
                std::cout << ".";
        }
        std::cout << std::endl;
    }
}

/********************************************************************
 * PART I
 * */
std::pair<int, int> direct_neighbours(
    const std::vector<uint8_t> map,
    const int i0,
    const int j0,
    const int N,
    const int M
) {
    int Nempty = 0, Noccupied = 0;
    uint8_t status;
    for (auto i = std::max(0, i0-1); i < std::min(N, i0+2); ++i) {
        // std::cout << "i0=" << i0 << ", i=" << i << std::endl;
        for (auto j = std::max(0, j0-1); j < std::min(M, j0+2); ++j) {
            if ((i == i0) && (j == j0))
                continue;
            status = map[ijk(i, j, M)];
            if (status == EMPTY)
                ++Nempty;
            if (status == OCCUPIED)
                ++Noccupied;
        }
    }
    // std::cout << "Found " << Nempty << ", " << Noccupied <<" around " << i0 << ", " << j0 << std::endl;
    return {Nempty, Noccupied};
}
std::pair<int, std::vector<uint8_t> >
evolve_game_of_life(
    const std::vector<uint8_t> map,
    const int N,
    const int M
) {
    auto new_map = map;
    int Nempty, Noccupied;
    int Nchanges = 0;
    for (int i = 0; i < N; ++i){
        for (int j = 0; j < M; ++j) {
            uint8_t status = map[ijk(i, j, M)];
            if (status == FLOOR)
                continue;
            else {
                std::tie(Nempty, Noccupied) = direct_neighbours(map, i, j, N, M);
                if ((status == EMPTY) && (Noccupied == 0)) {
                    new_map[ijk(i, j, M)] = OCCUPIED;
                    ++Nchanges;
                } else if ((status == OCCUPIED) && (Noccupied >= 4)) {
                    new_map[ijk(i, j, M)] = EMPTY;
                    ++Nchanges;
                }
            }
        }
    }
    return {Nchanges, new_map};
}

/********************************************************************
 * PART II
 * */
std::pair<int, int> distant_neighbours(
    const std::vector<uint8_t> map,
    const int i0,
    const int j0,
    const int N,
    const int M
) {
    int Nempty = 0, Noccupied = 0;
    uint8_t status;
    int i, j;
    for (auto di = -1; di <= 1; ++di) {
        for (auto dj = -1; dj <= 1; ++dj) {
            if (di == 0 && dj == 0)
                continue;
            i = i0+di;
            j = j0+dj;
            while (i >= 0 && i < N && j >= 0 && j < M) {
                status = map[ijk(i, j, M)];
                if (status == OCCUPIED) {
                    Noccupied++;
                    break;
                } else if (status == EMPTY) {
                    Nempty++;
                    break;
                }

                i += di;
                j += dj;
            }
        }
    }
    return {Nempty, Noccupied};

}
std::pair<int, std::vector<uint8_t> >
evolve_game_of_life_2(
    const std::vector<uint8_t> map,
    const int N,
    const int M
) {
    auto new_map = map;
    int Nempty, Noccupied;
    int Nchanges = 0;
    for (int i = 0; i < N; ++i){
        for (int j = 0; j < M; ++j) {
            uint8_t status = map[ijk(i, j, M)];
            if (status == FLOOR)
                continue;
            else {
                if ((status == EMPTY)) {
                    std::tie(Nempty, Noccupied) = distant_neighbours(map, i, j, N, M);
                    if (Noccupied == 0) {
                        new_map[ijk(i, j, M)] = OCCUPIED;
                        ++Nchanges;
                    }
                } else if ((status == OCCUPIED)) {
                    std::tie(Nempty, Noccupied) = distant_neighbours(map, i, j, N, M);
                    if (Noccupied >= 5) {
                        new_map[ijk(i, j, M)] = EMPTY;
                        ++Nchanges;
                    }
                }
            }
        }
    }
    return {Nchanges, new_map};
}
void find_fix_point(
        std::vector<uint8_t> map,
        const int N,
        const int M,
        std::pair<int, std::vector<uint8_t> > evolve (std::vector<uint8_t>, int, int)
) {
    std::vector<uint8_t> old_map = map;
    std::vector<uint8_t> new_map;
    int Nchanges = 1, iteration = 0;
    while (Nchanges > 0) {
        // print_map(old_map, N, M);
        std::tie(Nchanges, new_map) = evolve(old_map, N, M);
        std::cout << "#" << iteration << ": Nchange=" << Nchanges <<std::endl;
        iteration++;
        old_map = new_map;
    }
    // print_map(old_map, N, M);

    // We have a fixed point, count number of empty seats
    int Noccupied = 0;
    for (auto i = 0; i < N; ++i) {
        for (auto j = 0; j < M; ++j) {
             Noccupied += (old_map[ijk(i, j, M)] == OCCUPIED) ? 1 : 0;
        }
    }

    std::cout << "There are " << Noccupied << " occupied seats." << std::endl;
}

int main() {
    std::vector<int> numbers;
    numbers.push_back(0);
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;
    std::vector<std::string> lines;

    // Read first line to know size of array
    while(std::getline(myfile, line))
        lines.push_back(line);
    myfile.close();

    std::vector<uint8_t> map;
    char c;
    int i = -1, j = -1;
    int N, M = 0;
    N = lines.size();
    for (i = 0; line = lines[i], i < N; ++i) {
        M = line.size();
        if (map.size() == 0)
            map.assign(N*M, 0);
        for (j = 0; c = line[j], j < M; ++j) {
            map[ijk(i, j, M)] = (c == 'L') ? EMPTY : FLOOR;
        }
    }

    find_fix_point(map, N, M, evolve_game_of_life);
    find_fix_point(map, N, M, evolve_game_of_life_2);
}
