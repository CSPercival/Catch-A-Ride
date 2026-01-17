#pragma once

#include <fstream>
#include <vector>

#include "shared_structs/lites.hpp"

using namespace std;

struct Destination_Lists_Writer{
    ofstream file;
    vector<char> buffer;

    Destination_Lists_Writer(string directory_path, string file_name, int number_of_stops, bool create_header);
    void write_content(vector<Time_lite> &reach_times, vector<pair<Stop_lite, Trip_lite>> &predecessors);
    void copy_from_file(string file_path);
    void destructor();
};