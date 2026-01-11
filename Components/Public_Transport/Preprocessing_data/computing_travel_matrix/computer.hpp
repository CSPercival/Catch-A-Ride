#pragma once

#include "structs/lites.hpp"
#include "structs/stops.hpp"
#include "structs/trips.hpp"

void compute_travel_vector(Vertex_lite start, Stops *stop_data, Trips *trip_data, vector<vector<double>> *walk_matrix, vector<Time_lite> &visited, vector<pair<Stop_lite, Trip_lite>> &predecessor);
