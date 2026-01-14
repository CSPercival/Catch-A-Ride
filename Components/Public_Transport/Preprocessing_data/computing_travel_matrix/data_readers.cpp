#include <fstream>

#include "computing_travel_matrix/data_readers.hpp"

using json = nlohmann::json;

void read_stops(string path, Stops *stop_data){
    ifstream file(path);
    if (!file) throw std::runtime_error("Cannot open Stops");
    json j;
    file >> j;
    file.close();
    (*stop_data) = j.get<Stops>();
}

void read_trips(string path, Trips *trip_data){
    ifstream file(path);
    if (!file) throw std::runtime_error("Cannot open Trips");
    json j;
    file >> j;
    file.close();
    (*trip_data) = j.get<Trips>();
}

void read_walk_matrix(string path, vector<vector<double>> *walk_matrix){
    ifstream file(path);
    if (!file) throw std::runtime_error("Cannot open Trips");
    json j;
    file >> j;
    file.close();
    (*walk_matrix) = j.get<vector<vector<double>>>();
}
