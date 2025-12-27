#ifndef TRIP_STRUCT
#define TRIP_STRUCT

#include<iostream>
#include<string>

#include"Lites.hpp"

using namespace std;

struct Trip{
    Trip_lite id = -1;
    string line_name = "NN";
    vector<Vertex_lite> route;
    Trip() {}
    Trip(Trip_lite in_id, string &in_name) : id(in_id), line_name(in_name) {}
};

#endif