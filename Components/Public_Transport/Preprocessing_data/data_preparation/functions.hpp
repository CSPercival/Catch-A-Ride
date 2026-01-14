#ifndef FUNCTIONS
#define FUNCTIONS

#include<string>
#include<vector>

#include "shared_structs/lites.hpp"

using namespace std;

void split_string(string &line, char splitter, vector<string> &ans);
Time_lite string2time(string t);

#endif