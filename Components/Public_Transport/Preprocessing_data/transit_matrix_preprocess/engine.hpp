#pragma once

#include "shared_structs/lites.hpp"
#include "shared_structs/stops.hpp"
#include "shared_structs/trips.hpp"

void compute_travel_vector(Vertex_lite start, Stops *stop_data, vector<vector<double>> *walk_matrix, vector<Time_lite> &visited, vector<pair<Stop_lite, Trip_lite>> &predecessor);
