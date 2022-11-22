# include <vector>
# include <string>
# include <fstream>
# include <iostream>
# include <math.h>
# include <set>
# include <map>

int count_any_answer_questions(std::vector<std::string> answers) {
    // Count for each group the number of questions anyone answered
    int count = 0;
    std::set<char> questions;
    for (auto ans : answers) {
        if (ans == "") {
            count += questions.size();
            questions.clear();
        } else {
            for (auto q : ans) {
                questions.insert(q);
            }
        }
    }
    count += questions.size();
    return count;
}

int count_in_dict(const std::map<char, int> dict, const int expected_count) {
    int match_count = 0;
    for (auto const& [key, count] : dict) {
        if (count == expected_count)
            match_count += 1;
    }
    return match_count;
}

int count_all_answer_questions(std::vector<std::string> answers) {
    int count = 0;
    int group_size = 0;
    std::map<char, int> questions;
    for (auto ans : answers) {
        if (ans == "") {
            count += count_in_dict(questions, group_size);
            group_size = 0;
            questions.clear();
        } else {
            group_size += 1;
            for (auto q : ans) {
                auto search = questions.find(q);
                if (search != questions.end()) {
                    search->second += 1;
                } else {
                    questions[q] = 1;
                }
            }
        }
    }
    if (group_size > 0) {
        count += count_in_dict(questions, group_size);
    }
    return count;
}


int main() {
    // Load the boarding passes into a vector of strings
    std::vector<std::string> answers;
    std::fstream myfile("input", std::ios_base::in);
    std::string line;
    while(std::getline(myfile, line)){
        answers.push_back(line);
    }
    myfile.close();

    std::cout << "Number of questions answered by anyone in group " << count_any_answer_questions(answers) << "." << std::endl;
    std::cout << "Number of questions answered by all in group " << count_all_answer_questions(answers) << "." << std::endl;
}
