# include <fstream>
# include <string>
# include <algorithm>
# include <iostream>
# include <vector>

const std::string input_file = "input";

void find_first_bus(std::vector<int> bus_lines, int timestamp) {
    // std::vector<int> time_to_departure;
    int line, dt, dtmin, imin;
    dtmin = timestamp;
    imin = bus_lines.size();

    for (auto i = 0; i < bus_lines.size(); ++i) {
        line = bus_lines[i];
        if (line == 0)
            dt = timestamp;
        else
            dt = (timestamp / line + 1) * line - timestamp;

        if (dt < dtmin) {
            dtmin = dt;
            imin = i;
        }
        // time_to_departure.push_back(dt);
        std::cout << "Line #" << line << " : " << dt << std::endl;
    }
    std::cout << "Next to depart: bus #" << bus_lines[imin] << " in ";
    std::cout << dtmin << "min.";
    std::cout << " Product: " << dtmin * bus_lines[imin] << std::endl;
}

int main () {
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;
    std::vector<std::string> lines;

    // Parse timestamp
    std::getline(myfile, line);
    int timestamp = std::stoi(line);

    // Parse bus lines
    std::vector<int> bus_lines;
    std::getline(myfile, line);
    size_t istart = 0, iend = 0;

    while (iend != std::string::npos) {
        iend = line.find(",", istart);
        auto element = line.substr(istart, iend-istart);

        if (element == "x")
            bus_lines.push_back(0);
        else
            bus_lines.push_back(std::stoi(element));
        istart = iend + 1;
    }

    find_first_bus(bus_lines, timestamp);

}
