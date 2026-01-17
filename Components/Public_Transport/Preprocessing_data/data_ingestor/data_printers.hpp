#pragma once

#include<string>
#include "shared_structs/stops.hpp"
#include "shared_structs/trips.hpp"

using namespace std;

void print_stops(string path, Stops *stop_data);
void print_trips(string path, Trips *trip_data);
