#pragma once

#include<string>
#include "structs/stops.hpp"
#include "structs/trips.hpp"

using namespace std;

void print_stops(string path, Stops *stop_data);
void print_trips(string path, Trips *trip_data);
