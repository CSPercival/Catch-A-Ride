#include<fstream>
#include<iostream>
#include<vector>
#include<assert.h>

#include "consts.hpp"
#include "data_preparation/data_parsers.hpp"
#include "data_preparation/functions.hpp"
#include "shared_structs/day.hpp"

using namespace std;

void parse_stops(string &path, Stops *stop_data){
    Stop_lite new_id;
    string old_id, name;
    string line;
    vector<string> parts;
    ifstream file(path);
    getline(file, line);
    while(getline(file, line)){
        split_string(line, ',', parts);
        old_id = parts[0];
        new_id = (Stop_lite)stop_data->stops.size();
        name = parts[2];
        assert(!stop_data->id_mapping.count(old_id));
        stop_data->id_mapping[old_id] = new_id;
        stop_data->name_mapping[name].push_back(new_id);
        stop_data->stops.push_back(Stop(new_id, old_id, name, parts[3], parts[4]));
    }
    stop_data->number_of_stops = (int)stop_data->stops.size() - 1;
}

void parse_trips(string &path, Trips *trip_data){
    int trip_day_variant;
    Trip_lite new_id;
    string old_id, line_name;
    Day days[] = {trip_data->day - 1, trip_data->day, trip_data->day + 1};
    string line;
    vector<string> parts;
    ifstream trips_file(path);
    getline(trips_file, line);
    while(getline(trips_file, line)){
        split_string(line, ',', parts);
        trip_day_variant = stoi(parts[1]);
        for(int i = 0; i < 2; i++){
            if(days[i].variant != trip_day_variant) continue;
            old_id = parts[2] + trip_id_endings[i];
            new_id = (Trip_lite)trip_data->trips.size();
            line_name = parts[0];
            assert(!trip_data->id_mapping.count(old_id));
            trip_data->id_mapping[old_id] = new_id;
            trip_data->line_name_mapping[line_name].push_back(new_id);
            trip_data->trips.push_back(Trip(new_id, old_id, line_name, i));
        }
    }
    trip_data->number_of_trips = (int)trip_data->trips.size() - 1;
}

void parse_stop_times(string &path, Stops *stop_data, Trips *trip_data){
    int trip_day_variant;
    Stop_lite new_stop_id;
    Trip_lite new_trip_id;
    string old_trip_id, old_stop_id;
    Day days[] = {trip_data->day - 1, trip_data->day, trip_data->day + 1};
    string line;
    vector<string> parts;
    ifstream stop_times_file(path);
    getline(stop_times_file, line);
    while(getline(stop_times_file, line)){
        split_string(line, ',', parts);
        trip_day_variant = parts[0][0] - '0';
        for(int i = 0; i < 2; i++){
            if(days[i].variant != trip_day_variant) continue;
            old_trip_id = parts[0] + trip_id_endings[i];
            old_stop_id = parts[3];

            assert(stop_data->id_mapping.count(old_stop_id));
            assert(trip_data->id_mapping.count(old_trip_id));

            new_stop_id = stop_data->id_mapping[old_stop_id];
            new_trip_id = trip_data->id_mapping[old_trip_id];
            trip_data->trips[new_trip_id].route.push_back(
                Vertex_lite(new_stop_id, string2time(parts[1]) + (Time_lite)time_shifts[i])
            );
        }
    }
}

void prepare_structs(Stops *stop_data, Trips *trip_data){
    stop_data->stops.resize(1); // stops are 1 - indexed
    stop_data->stops[0].id = 0;
    for(int day_id = 0; day_id < days_num; day_id++){
        trip_data[day_id].trips.resize(1); // trips are 1 - indexed
        trip_data[day_id].trips[0].id = 0;
        trip_data[day_id].day = Day(day_id);
    }
}