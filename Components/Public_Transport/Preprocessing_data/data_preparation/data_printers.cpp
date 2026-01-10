#include "data_printers.hpp"
#include <fstream>

using json = nlohmann::json;

void print_stops(string path, Stops *stop_data){
    json j = (*stop_data);
    ofstream file(path);
    file << j.dump(4);
    file.close();
}

void print_trips(string path, Trips *trip_data){
    json j = (*trip_data);
    ofstream file(path);
    file << j.dump(4);
    file.close();
}