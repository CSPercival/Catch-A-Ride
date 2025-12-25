#include<fstream>
#include<iostream>
#include<vector>
#include<assert.h>

#include "data_reader.hpp"
#include "functions.hpp"

using namespace std;

void read_stops(string &path, Data *pt_data){
    string line;
    vector<string> parts;
    ifstream file(path);
    getline(file, line);
    int old_id;
    Stop_lite new_id;
    while(getline(file, line)){
        split_string(line, ',', parts);
        
        old_id = stoi(parts[0]);
        new_id = (Stop_lite)pt_data->stops.size();
        assert(!pt_data->o2n_stop.count(old_id));
        pt_data->o2n_stop[old_id] = new_id;
        pt_data->n2o_stop[new_id] = old_id;

        pt_data->stops.push_back(Stop(new_id, parts[2], parts[3], parts[4]));
    }
}

void read_trips(string &path, Data *pt_data, int day_id){
    string line;
    vector<string> parts;
    ifstream trips_file(path);
    getline(trips_file, line);
    Trip_lite new_id;
    string old_id;
    while(getline(trips_file, line)){
        split_string(line, ',', parts);
        
        if(stoi(parts[1]) != day_id) continue;

        old_id = parts[2];
        new_id = (Trip_lite)pt_data->trips.size();
        assert(!pt_data->o2n_trip.count(old_id));
        pt_data->o2n_trip[old_id] = new_id;
        pt_data->n2o_trip[new_id] = old_id;

        pt_data->trips.push_back(Trip(new_id, parts[0]));
    }
}

void read_stop_times(string &path, Data *pt_data, int day_id){
    string line;
    vector<string> parts;
    ifstream stop_times_file(path);
    getline(stop_times_file, line);
    while(getline(stop_times_file, line)){
        split_string(line, ',', parts);
        if(parts[0][0] - '0' != day_id) continue;
        assert(pt_data->o2n_stop.count(stoi(parts[3])));
        assert(pt_data->o2n_trip.count(parts[0]));
        assert(pt_data->o2n_stop[stoi(parts[3])] < (int)pt_data->stops.size());
        assert(pt_data->o2n_trip[parts[0]] < (int)pt_data->trips.size());
        pt_data->trips[pt_data->o2n_trip[parts[0]]].route.push_back(
            Vertex_lite(pt_data->o2n_stop[stoi(parts[3])], Time_lite(parts[1]))
        );
    }
}

void read_data(string stops_path, string trips_path, string stop_times_path, Data *pt_data, int day_id){
    pt_data->stops.resize(1);    // stops are 1-indexed
    pt_data->stops[0].id = 0;
    pt_data->trips.resize(1);    // trips are 1-indexed
    pt_data->trips[0].id = 0;

    read_stops(stops_path, pt_data);
    read_trips(trips_path, pt_data, day_id);
    read_stop_times(stop_times_path, pt_data, day_id);
}

void validate_data(Data *pt_data){
    for(auto &stop : pt_data->stops){
        assert(stop.id < stops_lim);
        assert(stop.id != -1);
    }
    int day_line_ctr = 0;
    for(auto &trip : pt_data->trips){
        assert(trip.id != -1);
        assert((int)trip.route.size() > 0 || trip.id == 0);
        // if(trip.route.size() == 0){
        //     trip.print();
        //     assert(false);
        // }
        day_line_ctr = 0;
        for(int i = 1; i < (int)trip.route.size(); i++){
            if(trip.route[i].time < trip.route[i - 1].time) day_line_ctr++;
        }
        assert(day_line_ctr < 2);
    }
}