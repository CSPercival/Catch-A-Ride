#ifndef DATA_WRITER
#define DATA_WRITER

#include <fstream>
#include <vector>

#include "structs/Data.hpp"
#include "structs/Lites.hpp"
#include "structs/Stop.hpp"
#include "structs/Trip.hpp"

using namespace std;

struct Destination_Lists_Writer{
    ofstream file;

    Destination_Lists_Writer(string directory_path, string file_name);
    void write_content(vector<Time_lite> &reach_times, vector<pair<Stop_lite, Trip_lite>> &predecessors);
    void destructor();
};

struct Stops_Data_Writer{
    ofstream file;

    Stops_Data_Writer(string directory_path, string file_name);
    void write_content(Stop &stop);
    void destructor();
};

struct Trips_Data_Writer{
    ofstream file;

    Trips_Data_Writer(string directory_path, string file_name, int day_id);
    void write_content(Trip &trip);
    void destructor();
};


#endif