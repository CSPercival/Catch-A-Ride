#include <iostream>
#include <filesystem>

#include "data_parsers.hpp"
#include "data_printers.hpp"
#include "structs/stops.hpp"
#include "structs/trips.hpp"

using namespace std;

Stops stop_data;
Trips trip_data[days_num];

int main(){
    string resources_path = "./../Resources/";
    string stops_path = resources_path + "GTFS/stops.txt";
    string trips_path = resources_path + "GTFS/trips.txt";
    string stop_times_path = resources_path + "GTFS/stop_times.txt";

    cerr << "START\n";
    prepare_structs(&stop_data, trip_data);
    cerr << "PARSING...\n";
    parse_stops(stops_path, &stop_data);
    cerr << "    #0 Stage\n";
    for(int day_id = 0; day_id < days_num; day_id++){
        parse_trips(trips_path, &trip_data[day_id]);
        parse_stop_times(stop_times_path, &stop_data, &trip_data[day_id]);
        cerr << "    #" << day_id + 1 << " Stage\n";
    }
    cerr << "PRINTING...\n";
    filesystem::create_directories(resources_path + "Preprocessed_Data/Common");
    print_stops(resources_path + "Preprocessed_Data/Common/Stops.json", &stop_data);
    cerr << "    #0 Stage\n";
    for(int day_id = 0; day_id < days_num; day_id++){
        filesystem::create_directories(resources_path + "Preprocessed_Data/" + day_names[day_id]);
        print_trips(resources_path + "Preprocessed_Data/" + day_names[day_id] + "/Trips.json", &trip_data[day_id]);
        cerr << "    #" << day_id + 1 << " Stage\n";
    }
}