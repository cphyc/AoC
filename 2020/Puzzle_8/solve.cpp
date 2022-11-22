# include <iostream>
# include <fstream>
# include <string>
# include <vector>
# include <regex>

// Parse the line and return the new fp, acc
std::pair<int, int> parse_line(const std::string line, size_t fp, int acc) {
    const std::regex re("(acc|jmp|nop) ([-\\+]\\d*)");
    std::smatch m;
    std::regex_match(line, m, re);

    // std::cout << line << std::endl;
    // std::cout << "\tm[1]=" << m[1].str() << std::endl;

    std::string instruction = m[1].str();
    int value = std::stoi(m[2].str());
    // std::cout << "fp= " << fp << "\tinstruction=" << instruction << "\tvalue=" << value << "\tacc=" << acc << std::endl;

    if (instruction == "nop") {
        return {fp + 1, acc};
    } else if (instruction == "jmp") {
        return {fp + value, acc};
    } else if (instruction == "acc") {
        return {fp + 1, acc + value};
    } else {
        throw "Unknown instruction " + instruction;
    }
}

std::pair<int, int> read_until_double_instruction(const std::vector<std::string> lines, std::vector<int> execution_count) {
    // Now read the instruction
    int acc = 0, new_acc;
    size_t fp = 0, new_fp;
    size_t Ninstruction = lines.size();
    while (fp < Ninstruction && execution_count[fp] == 0) {
        ++execution_count[fp];
        std::tie(new_fp, new_acc) = parse_line(lines[fp], fp, acc);
        fp = new_fp;
        acc = new_acc;
    }
    return {fp, acc};
}

std::pair<int, int> find_double(const std::vector<std::pair<std::string, int>> instructions) {
    int acc = 0, new_acc;
    size_t fp = 0, new_fp;
    size_t Ninstruction = instructions.size();
    std::vector<int> execution_count;
    std::pair<std::string, int> instruction;

    execution_count.assign(instructions.size(), 0);
    while (fp < Ninstruction && execution_count[fp] == 0) {
        ++execution_count[fp];
        instruction = instructions[fp];
        if (instruction.first == "nop")
            fp++;
        else if (instruction.first == "jmp")
            fp += instruction.second;
        else if (instruction.first == "acc") {
            fp++;
            acc += instruction.second;
        }
    }
    return {fp, acc};
}


typedef std::pair<std::string, int> inst_t;
typedef std::map<inst_t, std::vector<std::pair<int, inst_t>>> inst_tree_t;

void add_link(const inst_t inst, const std::vector<inst_t> instructions, inst_tree_t & tree, int fp) {
    auto jmp = ((inst.first == "jmp") ? inst.second : 1);
    auto next_fp = fp + jmp;
    inst_t next_inst;
    if (next_fp >= instructions.size())
        next_inst = {"END", instructions.size()};
    else {
        next_inst = instructions[next_fp];
    }
    tree[inst].push_back({jmp, next_inst});
}

inst_tree_t build_tree(const std::vector<inst_t> instructions) {
    inst_tree_t tree;
    int N = instructions.size();

    inst_t inst1, inst2, inst3;
    int jmp;

    for (size_t i = 1; i < instructions.size(); ++i) {
        inst1 = instructions[i];
        add_link(inst1, instructions, tree, i);

        if (inst1.first != "acc") {
            inst2 = {
                (inst1.first == "jmp") ? "nop" : "jmp",
                inst1.second
            };
            tree[inst1].push_back({N, inst2});
            add_link(inst2, instructions, tree, i);
        }
    }
    return tree;
}
// std::vector<std::string> swap_instruction(const std::vector<std::string> lines, int index) {
//     std::vector<std::string> output_lines;
//     output_lines = lines;
//     const std::regex re("(jmp|nop) ([-\\+]\\d*)");
//     std::smatch m;
//     int j = 0;
//     std::string line;
//     for (size_t i = 0; i < output_lines.size(); ++i) {
//         line = output_lines[i];
//         if (std::regex_match(line, m, re)) {
//             if (j == index) {
//                 if (m[1].str() == "jmp")
//                     line = "nop " + m[2].str();
//                 else
//                     line = "jmp " + m[2].str();

//                 std::cout << "was: " << lines[i] << "\tnow: " << line << std::endl;
//                 output_lines[i] = line;
//                 break;
//             }
//             ++j;
//         }
//     }
//     return output_lines;
// }

// std::pair<int, int> fix_program(const std::vector<std::string> lines, std::vector<int> execution_count) {
//     const int Ninstruction = lines.size();
//     int fp = 0, acc, index = 0;

//     while (fp < Ninstruction) {
//         execution_count.assign(execution_count.size(), 0);
//         auto new_lines = swap_instruction(lines, index);
//         std::tie(fp, acc) = read_until_double_instruction(new_lines, execution_count);
//         ++index;
//     }
//     return {index, acc};

// }

int main() {
    std::vector<std::pair<std::string, int>> instructions;
    std::fstream myfile("input", std::ios_base::in);
    std::string line;
    const std::regex re("(acc|jmp|nop) ([-\\+]\\d*)");
    std::smatch m;
    while(std::getline(myfile, line)){
        std::regex_match(line, m, re);
        instructions.push_back({m[1].str(), std::stoi(m[2].str())});
    }
    myfile.close();

    std::cout << "Before the first doubled instruction, the accumulator value was " << find_double(instructions).second << std::endl;
    // auto ret = fix_program(lines, execution_count);
    // std::cout << "Need to swap line " << ret.first << ", accumulator is now: " << ret.second << std::endl;
}
