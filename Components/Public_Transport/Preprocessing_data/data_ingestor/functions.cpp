#include "data_ingestor/functions.hpp"

void split_string(string &line, char splitter, vector<string> &ans){
    ans.clear();
    int last_splitter = -1;
    line.push_back(',');
    for(int i = 0; i < (int)line.size(); i++){
        if(line[i] == splitter){
            ans.push_back(line.substr(last_splitter + 1, i - last_splitter - 1));
            while(!ans.back().empty() && ans.back().back() < 32) ans.back().pop_back();
            last_splitter = i;
        }
    }
    line.pop_back();
}

Time_lite string2time(string t){
    return (Time_lite)(stoi(t.substr(0, 2)) * 60 + stoi(t.substr(3, 2)));
}