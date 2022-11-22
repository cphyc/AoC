# include <vector>
# include <string>
# include <fstream>
# include <iostream>
# include <math.h>


std::pair<int, int> find_seat(std::string boarding_pass){
    std::pair<int, int> seat;
    int row = 0, col = 0;

    // Now we loop through the boarding pass
    for (auto s: boarding_pass){
        switch (s)
        {
        case 'B':
            row <<= 1;
            row += 1;
            break;
        case 'F':
            row <<= 1;
            break;
        case 'R':
            col <<= 1;
            col += 1;
            break;
        case 'L':
            col <<= 1;
            break;
        }
    }
    seat.first = row;
    seat.second = col;
    return seat;
}


int main() {
    // Load the boarding passes into a vector of strings
    std::vector<std::string> boarding_passes;
    std::fstream myfile("input", std::ios_base::in);
    std::string line;
    while(std::getline(myfile, line)){
        boarding_passes.push_back(line);
    }
    myfile.close();

    // Loop through and calculate the seat ids from the boarding passes
    std::pair<int, int> seat;
    int id, ans1;
    ans1 = -1;
    for(auto bp : boarding_passes){
        seat = find_seat(bp);
        id = seat.first*8+seat.second;
        ans1 = std::max(ans1, id);
    }
    std::cout << "ans1: " << ans1 << std::endl;
}
