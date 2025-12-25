#ifndef DATA_STRUCT
#define DATA_STRUCT

#include<iostream>
#include<string>
#include<vector>
#include<map>

#include "Stop.hpp"
#include "Trip.hpp"
#include "Lites.hpp"

using namespace std;

struct Data{
    map<int, Stop_lite> o2n_stop;
    map<Stop_lite, int> n2o_stop;
    map<string, Trip_lite> o2n_trip;
    map<Trip_lite, string> n2o_trip;
    vector<Stop> stops;
    vector<Trip> trips;
    inline static vector<vector<Time_lite>> walk_matrix;
    inline static bool walk_matrix_computed = false;
    Data(){}
};

#endif