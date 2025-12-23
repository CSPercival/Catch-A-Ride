#include "functions.hpp"

void split_string(string &line, char splitter, vector<string> &ans){
    ans.clear();
    int last_splitter = -1;
    line.push_back(',');
    for(int i = 0; i < (int)line.size(); i++){
        if(line[i] == splitter){
            ans.push_back(line.substr(last_splitter + 1, i - last_splitter - 1));
            last_splitter = i;
        }
    }
    line.pop_back();
}