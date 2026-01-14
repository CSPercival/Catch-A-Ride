#pragma once

#include<string>

#include "shared_structs/stops.hpp"
#include "shared_structs/trips.hpp"

using namespace std;

void prepare_structs(Stops *stop_data, Trips *trip_data);
void parse_stops(string &stops_path, Stops *stop_data);
void parse_trips(string &trips_path, Trips *trip_data);
void parse_stop_times(string &stop_times_path, Stops *stop_data, Trips *trip_data);
