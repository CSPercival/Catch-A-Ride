#ifndef DATA_STRUCT
#define DATA_STRUCT

#include<iostream>
#include<string>
#include<vector>
#include<map>

#include "Stop.hpp"
#include "Trip.hpp"
#include "Lites.hpp"
#include "Day.hpp"

using namespace std;

struct Data{
    Day id; // present day
    map<int, Stop_lite> o2n_stop;
    map<Stop_lite, int> n2o_stop;
    map<string, Trip_lite> o2n_trip;
    map<Trip_lite, string> n2o_trip;
    vector<Stop> stops;
    vector<Trip> trips;
    inline static vector<vector<Time_lite>> walk_matrix;
    Data(){}
};

#endif