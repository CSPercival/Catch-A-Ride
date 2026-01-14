#pragma once

#include<iostream>
#include<string>
#include<vector>
#include<map>
#include<optional>
#include <nlohmann/json.hpp>

#include "lites.hpp"

using namespace std;

struct Stop{
    Stop_lite id = -1;
    string old_id = "0";
    string name = "NN";
    string lat = "0.0", lng = "0.0";
    optional<vector<Stop_lite>> reachable;
    optional<vector<vector<Edge_lite>>> connections;
    Stop() {}
    Stop(Stop_lite in_id, string &in_old_id, string &in_name, string &in_lat, string &in_lng) : id(in_id), old_id(in_old_id), name(in_name), lat(in_lat), lng(in_lng) {};
    Edge_lite get_next(Time_lite u_time, Stop_lite v_id);
    void print_all();
    void print_name();
};

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Stop,
    id,
    old_id,
    name,
    lat,
    lng
)

struct Stops{
    int number_of_stops;
    map<string, Stop_lite> id_mapping;
    map<string, vector<Stop_lite>> name_mapping;
    vector<Stop> stops;
};


NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Stops,
    number_of_stops,
    id_mapping,
    name_mapping,
    stops
)