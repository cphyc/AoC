# include <iostream>
# include <fstream>
# include <regex>
# include <string>
# include <map>
# include <set>
# include <queue>

typedef std::pair<std::string, std::string> string_pair;
typedef std::tuple<int, std::string, std::string> bag_info;
typedef std::map<string_pair, std::set<bag_info>> bag_tree;

void parse_line(const std::string line, bag_tree & tree) {
    std::smatch match;

    const std::regex re(
        "([a-z]+) ([a-z]+) bags contain (([0-9] [a-z]+ [a-z]+ bags?[,\\. ]+)+|no other bags\\.)"
    );
    const std::regex re_bags(
        "([0-9]) ([a-z]+) ([a-z]+) bags?[(, )\\.]"
    );

    if (std::regex_match(line, match, re)) {
        if (match.size() == 0) {
            std::string err = "Could not match line: " + line;
            throw err;
        }
        string_pair bag = {match[1].str(), match[2].str()};

        std::set<bag_info> bag_set = {};
        if (match[4].matched) {
            // Bag contains other bags
            std::smatch sub_bag_match;
            std::string bag_str = match[3].str();
            while (std::regex_search(bag_str, sub_bag_match, re_bags)) {
                int Nbag = std::stoi(sub_bag_match[1].str());
                bag_info sub_bag = std::make_tuple(
                    Nbag,
                    sub_bag_match[2].str(),
                    sub_bag_match[3].str()
                );
                bag_set.insert(sub_bag);
                bag_str = sub_bag_match.suffix();
                // std::cout << "HERE!" << sub_bag.first << ", " << sub_bag.second << std::endl;
            }
        }

        tree[bag] = bag_set;
    }
}

void print_tree(bag_tree const tree) {
    for (auto const& [key, bag_set] : tree) {
        std::cout << key.first << "." << key.second << ":\t";
        for (auto bag: bag_set) {
            std::cout << std::get<1>(bag) << "." << std::get<2>(bag);
            std::cout << "(" << std::get<0>(bag) << "), ";
        }

        std::cout << std::endl;
    }
}

std::set<string_pair> get_containers(const bag_tree tree, const string_pair bag) {
    std::queue<string_pair> bags_to_explore;
    std::set<string_pair> parent_bags = {};

    bags_to_explore.push(bag);
    while (bags_to_explore.size() > 0) {
        auto b = bags_to_explore.front();
        bags_to_explore.pop();

        // Find possible parents in the tree
        for (auto const & [key, bset]: tree) {
            for (auto tmp: bset) {
                if (std::get<1>(tmp) == b.first && std::get<2>(tmp) == b.second) {
                    // If the parent bag is *not* already in the parents, explore it
                    if (!parent_bags.contains(key)) {
                        parent_bags.insert(key);
                        bags_to_explore.push(key);
                        break;
                    }
                }
            }
        }
    }
    return parent_bags;
}

int count_nested_bags(const bag_tree tree, const string_pair bag) {
    std::queue<bag_info> bags_to_explore;
    int Ntot = 0;
    bag_info bi = std::make_tuple(1, bag.first, bag.second);
    bags_to_explore.push(bi);

    while (bags_to_explore.size() > 0) {
        auto b = bags_to_explore.front();
        int N = std::get<0>(b);
        string_pair bag_name = {std::get<1>(b), std::get<2>(b)};

        Ntot += N;
        bags_to_explore.pop();

        auto children_bags = tree.at(bag_name);

        for (const bag_info child: children_bags) {
            int Nchild = std::get<0>(child);
            string_pair bchild = {std::get<1>(child), std::get<2>(child)};
            bag_info new_child = std::make_tuple(N * Nchild, bchild.first, bchild.second);
            bags_to_explore.push(new_child);
        }
    }
    // We need to remove the initial bag
    return Ntot - 1;
}

void print_container(std::set<string_pair> set) {
    std::cout << "{";
    for (auto s: set)
        std::cout << s.first << "." << s.second << ", ";
    std::cout << "}";
}

int main() {
    // Load the boarding passes into a vector of strings
    std::vector<std::string> lines;
    std::fstream myfile("input", std::ios_base::in);
    std::string line;
    while(std::getline(myfile, line)){
        lines.push_back(line);
    }
    myfile.close();

    bag_tree tree;
    for (auto const line: lines) {
        parse_line(line, tree);
    }
    print_tree(tree);

    string_pair my_bag = {"shiny", "gold"};
    std::set<string_pair> parents = get_containers(tree, my_bag);
    std::cout << "Parents of shiny.gold: ";
    print_container(parents);
    std::cout << " (" << parents.size() << ")" << std::endl;

    std::cout << "One shiny.gold contains " << count_nested_bags(tree, my_bag) << " children!\n";
}
