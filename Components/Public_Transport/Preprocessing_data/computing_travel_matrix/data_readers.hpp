#pragma once

#include<string>
#include "structs/stops.hpp"
#include "structs/trips.hpp"

using namespace std;

void read_stops(string path, Stops *stop_data);
void read_trips(string path, Trips *trip_data);
void read_walk_matrix(string path, vector<vector<double>> *walk_matrix);
