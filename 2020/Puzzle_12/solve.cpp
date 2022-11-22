# include <vector>
# include <fstream>
# include <string>
# include <algorithm>
# include <map>
# include <iostream>
# include <set>

const std::string input_file = "input";


void move_ship(std::vector<std::pair<char, int>> instructions) {
 int east = 0;
    int north = 0;
    int angle = 0;
    char cmd;
    int dist;
    int i = 0;
    for (auto inst: instructions) {
        std::tie(cmd, dist) = inst;
        // std::cout << lines[i] << " : " << cmd << " " << dist << std::endl;
        ++i;
        if (cmd == 'F') {
            if (angle == 0)
                cmd = 'E';
            else if (angle == 90)
                cmd = 'S';
            else if (angle == 180)
                cmd = 'W';
            else if (angle == 270)
                cmd = 'N';
        }

        if (cmd == 'R') {
            angle += dist;
        } else if (cmd == 'L') {
            angle -= dist;
        } else if (cmd == 'N') {
            north += dist;
        } else if (cmd == 'S') {
            north -= dist;
        } else if (cmd == 'E') {
            east += dist;
        } else if (cmd == 'W') {
            east -= dist;
        }

        if (angle >= 360)
            angle -= 360;
        if (angle < 0)
            angle += 360;

        std::cout << "EAST " << east << "  NORTH " << north << " angle " << angle <<std::endl;
    }
    std::cout << "Manhattan distance: " << std::abs(east) + std::abs(north) << std::endl;
}

std::pair<int, int> rotate(int east, int north, int rotation) {
    while (rotation != 0) {
        if (rotation < 0) {
            auto tmp = east;
            east = -north;
            north = tmp;
            rotation += 90;
        } else {
            auto tmp = east;
            east = north;
            north = -tmp;
            rotation -= 90;
        }
    }
    return {east, north};
}

void move_ship_with_bearing(std::vector<std::pair<char, int>> instructions) {
    int east = 0;
    int north = 0;
    int wp_east = 10;
    int wp_north = 1;
    char cmd;
    int dist;
    for (auto inst: instructions) {
        std::tie(cmd, dist) = inst;
        if (cmd == 'F') {
            east += wp_east * dist;
            north += wp_north * dist;
        }

        if (cmd == 'R') {
            std::tie(wp_east, wp_north) = rotate(wp_east, wp_north, dist);
        } else if (cmd == 'L') {
            std::tie(wp_east, wp_north) = rotate(wp_east, wp_north, -dist);
        } else if (cmd == 'N') {
            wp_north += dist;
        } else if (cmd == 'S') {
            wp_north -= dist;
        } else if (cmd == 'E') {
            wp_east += dist;
        } else if (cmd == 'W') {
            wp_east -= dist;
        }
        std::cout << "EAST " << east << "  NORTH " << north  << "WP EAST" << wp_east << "  WP_NORTH" << wp_north << std::endl;
    }
    std::cout << "Manhattan distance: " << std::abs(east) + std::abs(north) << std::endl;
}

int main () {
    std::vector<std::pair<char, int>> instructions;
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;
    std::vector<std::string> lines;
    // Read first line to know size of array
    while(std::getline(myfile, line)) {
        instructions.push_back({
            line[0],
            std::stoi(line.substr(1, line.size()))
        });
        lines.push_back(line);
    }
    myfile.close();

    move_ship(instructions);
    move_ship_with_bearing(instructions);
}
