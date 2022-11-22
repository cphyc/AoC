# include <iostream>
# include <vector>

inline int const Ndigit = 30;
inline uint64_t const maski = 0b0'000000000000000000000000000000'111111111111111111111111111111;
inline uint64_t const maskc = 0b1'000000000000000000000000000000'000000000000000000000000000000;

int part_I(const std::vector<int> inputs, const int Nturn) {
    std::vector<uint64_t> counts(Nturn, 0);

    uint64_t ilast, next;
    uint64_t new_value;
    uint64_t imax = inputs.size();
    for (uint64_t i = 0; i < imax; ++i) {
       counts[inputs[i]] = maskc | (i << Ndigit) | i;
       next = 0;
    }
    uint64_t* it;
    for (uint64_t i = imax; i < Nturn-1; ++i) {
        it = &counts[next];
        new_value = maskc | i;
        if (*it & maskc) {
             ilast = (*it & maski);
            new_value |= (ilast << Ndigit);
            next = i - ilast;
        } else {
            next = 0;
        }
        *it = new_value;
    }
    std::cout << next << std::endl;
    return next;
}

int main() {
    part_I({0,1,5,10,3,12,19}, 2020);
    part_I({0,1,5,10,3,12,19}, 30'000'000);
}
