#pragma once

#include <fstream>
#include <vector>

#include "shared_structs/lites.hpp"

using namespace std;

struct Destination_Lists_Writer{
    ofstream file;

    Destination_Lists_Writer(string directory_path, string file_name, int number_of_stops);
    void write_content(vector<Time_lite> &reach_times, vector<pair<Stop_lite, Trip_lite>> &predecessors);
    void destructor();
};