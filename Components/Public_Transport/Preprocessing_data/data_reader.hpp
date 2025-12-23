#ifndef DATA_READER
#define DATA_READER

#include<bits/stdc++.h>
#include<fstream>
#include "structs.hpp"

using namespace std;

void split_string(string &line, char splitter, vector<string> &ans);

struct Data{
    map<int, int> trans_stop;
    map<string, int> trans_trip;
    // map<int, Stop> stops;
    // map<string, Trip> trips;
    vector<Stop> stops;
    vector<Trip> trips;
    Data(string stops_path, string trips_path, string stop_times_path);
    void run_checker();
};

#endif