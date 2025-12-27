#ifndef DATA_READER
#define DATA_READER

#include<string>

#include "structs/Data.hpp"

using namespace std;

void read_data(string stops_path, string trips_path, string stop_times_path, Data *data, int day_id);
void validate_data(Data *data);

#endif