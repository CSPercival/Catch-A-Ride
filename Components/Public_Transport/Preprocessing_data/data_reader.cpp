#include<fstream>
#include<iostream>
#include<vector>
#include<assert.h>

#include "consts.hpp"
#include "data_reader.hpp"
#include "functions.hpp"
#include "structs/Day.hpp"

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
        for(int day_id = 0; day_id < days_num; day_id++){
            new_id = (Stop_lite)pt_data[day_id].stops.size();
            assert(!pt_data[day_id].o2n_stop.count(old_id));
            pt_data[day_id].o2n_stop[old_id] = new_id;
            pt_data[day_id].n2o_stop[new_id] = old_id;
            stop_name_max = max(stop_name_max, (int)parts[2].size() + 1);
            latitude_max = max(latitude_max, (int)parts[3].size() + 1);
            longtitude_max = max(longtitude_max, (int)parts[4].size() + 1);
            pt_data[day_id].stops.push_back(Stop(new_id, parts[2], parts[3], parts[4]));
        }
    }
    stops_lim = (int)pt_data[0].stops.size();    
    for(int day_id = 0; day_id < days_num; day_id++){
        assert(stops_lim == (int)pt_data[day_id].stops.size());
        for(int i = 0; i < stops_lim; i++){
            pt_data[day_id].stops[i].connections.resize(stops_lim);
        }
    }
}

void read_trips(string &path, Data *pt_data){
    string line;
    vector<string> parts;
    int trip_day_variant;
    ifstream trips_file(path);
    getline(trips_file, line);
    Trip_lite new_id;
    string old_id;
    while(getline(trips_file, line)){
        split_string(line, ',', parts);
        trip_day_variant = stoi(parts[1]);

        Day days[] = {Day(1), Day(0), Day(-1)};
        for(int it = 0; it < days_num; it++, days[0] = days[0] + 1, days[1] = days[1] + 1, days[2] = days[2] + 1){
            if(days[1].variant == trip_day_variant){
                for(int it2 = 0; it2 < 3; it2++){
                    old_id = parts[2] + trip_id_endings[it2];

                    assert(!pt_data[days[it2].id].o2n_trip.count(old_id));
                    new_id = (Trip_lite)pt_data[days[it2].id].trips.size();
                    pt_data[days[it2].id].o2n_trip[old_id] = new_id;
                    pt_data[days[it2].id].n2o_trip[new_id] = old_id;

                    pt_data[days[it2].id].trips.push_back(Trip(new_id, parts[0]));
                }
            }
        }
        
        line_name_max = max(line_name_max, (int)parts[0].size() + 1);
    }
    for(int day_id = 0; day_id < days_num; day_id++){
        trips_lim[day_id] = (int)pt_data[day_id].trips.size();
    }
}

void read_stop_times(string &path, Data *pt_data){
    string line;
    vector<string> parts;
    ifstream stop_times_file(path);
    int trip_day_variant;
    getline(stop_times_file, line);
    while(getline(stop_times_file, line)){
        split_string(line, ',', parts);
        trip_day_variant = parts[0][0] - '0';

        Day days[] = {Day(1), Day(0), Day(-1)};
        for(int it = 0; it < days_num; it++, days[0] = days[0] + 1, days[1] = days[1] + 1, days[2] = days[2] + 1){
            if(days[1].variant == trip_day_variant){
                for(int it2 = 0; it2 < 3; it2++){
                    string old_id = parts[0] + trip_id_endings[it2];
                    assert(pt_data[days[it2].id].o2n_stop.count(stoi(parts[3])));
                    assert(pt_data[days[it2].id].o2n_trip.count(old_id));
                    assert(pt_data[days[it2].id].o2n_stop[stoi(parts[3])] < (int)pt_data[days[it2].id].stops.size());
                    assert(pt_data[days[it2].id].o2n_trip[old_id] < (int)pt_data[days[it2].id].trips.size());
                    pt_data[days[it2].id].trips[pt_data[days[it2].id].o2n_trip[old_id]].route.push_back(
                        Vertex_lite(pt_data[days[it2].id].o2n_stop[stoi(parts[3])], string2time(parts[1]) + (Time_lite)time_shifts[it2])
                        );
                }
            }
        }
    }
}

void read_data(string stops_path, string trips_path, string stop_times_path, Data *pt_data){
    for(int day_id = 0; day_id < days_num; day_id++){
        pt_data[day_id].stops.resize(1);    // stops are 1-indexed
        pt_data[day_id].stops[0].id = 0;
        pt_data[day_id].trips.resize(1);    // trips are 1-indexed
        pt_data[day_id].trips[0].id = 0;
    }
    read_stops(stops_path, pt_data);
    read_trips(trips_path, pt_data);
    read_stop_times(stop_times_path, pt_data);
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
        day_line_ctr = 0;
        for(int i = 1; i < (int)trip.route.size(); i++){
            if(trip.route[i].time < trip.route[i - 1].time) day_line_ctr++;
        }
        assert(day_line_ctr < 2);
    }
}