# include <fstream>
# include <string>
# include <iostream>
# include <vector>
# include <regex>
# include <map>
# include <functional>

std::regex line_re("(\\d+): (\"([a-z])\"|\\d+( ?\\|? \\d+)*)");
std::regex rule_re("\\d+|\\|");

void parse_rule(const std::string line, std::map<int, std::function<bool(const std::string, int&)>> &rules, bool debug=false) {
    std::smatch m;
    std::regex_match(line, m, line_re);
    int irule = std::stoi(m[1]);
    std::function<bool(const std::string, int&)> rule;
    if (m[3].str() != "") {
        // Rule defined by a single char
        char check_char = m[3].str()[0];
        rule = [=](std::string input, int& i) {
            for (auto j = 0; j < i; ++j) std::cout << ".";
            auto ret = (i < input.size()) && (input[i] == check_char);
            std::cout << "#" << irule << "->" << check_char << "? " << ret << std::endl;
            ++i;
            return ret;
        };
    } else {
        // Rule defined by reference to other rule(s)
        std::vector<std::vector<int>> rule_set = {};
        std::vector<int> rule_list = {};
        std::string rule_str = m[2].str();
        auto rule_begin = std::sregex_iterator(rule_str.begin(), rule_str.end(), rule_re);
        auto rule_end = std::sregex_iterator();

        for (auto it = rule_begin; it != rule_end; ++it) {
            auto match = *it;
            std::string match_string = match.str();
            if (match_string == "|") {
                std::vector<int> rl_copy = rule_list;
                rule_set.push_back(rl_copy);
                rule_list.clear();
            } else {
                rule_list.push_back(std::stoi(match_string));
            }
        }
        rule_set.push_back(rule_list);

        rule = [=, &rules](const std::string input, int& i) {
            std::cout << input << std::endl;
            for (auto j = 0; j < i; ++j) std::cout << ".";
            std::cout << "^ #" << irule << std::endl;
            if (irule == 11 || irule == 8) {
                // Do nothing
                std::cout << "HERE!" << std::endl;
            }
            bool ok;
            int j;
            // Test all possible rule combinations
            for (auto rs: rule_set) {
                j = i;
                // Check each rule is matched
                for (auto ir: rs) {
                    ok = rules[ir](input, j);
                    if (!ok) break;
                }
                if (irule == 0 && j != input.size()) ok = false;
                if (ok) {
                    i = j;
                    break;
                }
            }
            i = j;
            return ok;
        };
    }
    rules[irule] = rule;
}

bool check_line(const std::string line, std::function<bool(const std::string, int&)> rule) {
    int i = 0;
    auto ok = rule(line, i);
    return ok && i == line.size();
}

void part_I(std::map<int, std::function<bool(const std::string, int&)>> rules, std::vector<std::string> lines, bool verbose=false) {
    int Nok = 0;
    for (auto line: lines) {
        auto ok = check_line(line, rules[0]);
        if (verbose) std::cout << "Checking > " << line << ": " ;
        if (verbose) std::cout << ok << std::endl;
        if (ok) ++Nok;
    }
    std::cout << "Found " << Nok << " ok lines." << std::endl;
}


void solve(const std::string input_file, bool verbose=false) {
    std::vector<std::string> lines;
    std::fstream myfile(input_file, std::ios_base::in);
    std::string line;

    while (std::getline(myfile, line))
        lines.push_back(line);
    myfile.close();

    // Parse the rules
    int i = 0;
    std::map<int, std::function<bool(const std::string, int&)>> rules;
    for (line = lines[0], i = 0; line != ""; ++i, line = lines[i]) {
        parse_rule(line, rules);
    }
    ++i;
    // Parse the lines
    // std::vector<std::string> lines_to_check(lines.begin()+i, lines.end());
    std::vector<std::string> lines_to_check = {"babbbbaabbbbbabbbbbbaabaaabaaa"};
    part_I(rules, lines_to_check, verbose);
}

int main() {
    solve("input_test2", true);
    // solve("input_modified");
}
