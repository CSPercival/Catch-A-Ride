#include "data_reader.hpp"

void split_string(string &line, char splitter, vector<string> &ans){
    ans.clear();
    int last_splitter = -1;
    line.push_back(',');
    for(int i = 0; i < (int)line.size(); i++){
        if(line[i] == splitter){
            ans.push_back(line.substr(last_splitter + 1, i - last_splitter - 1));
            last_splitter = i;
        }
    }
    line.pop_back();
}

Data::Data(string stops_path, string trips_path, string stop_times_path){
    string line;
    vector<string> parts;
    stops.resize(1);    // stops are 1-indexed
    stops[0].id = 0;
    trips.resize(1);    // trips are 1-indexed
    trips[0].id = 0;

    ifstream stops_file(stops_path);
    getline(stops_file, line);
    while(getline(stops_file, line)){
        split_string(line, ',', parts);
        int old_id = stoi(parts[0]);
        assert(!trans_stop.count(old_id));
        trans_stop[old_id] = (int)trans_stop.size() + 1;
        // stops[trans_stop.size()] = Stop(trans_stop.size(), parts[2], parts[3], parts[4]);
        stops.push_back(Stop(trans_stop.size(), parts[2], parts[3], parts[4]));
        // stops.emplace(stoi(parts[0]), Stop(stoi(parts[0]), parts[2], stod(parts[3]), stod(parts[4])));
    }

    ifstream trips_file(trips_path);
    getline(trips_file, line);
    while(getline(trips_file, line)){
        split_string(line, ',', parts);
        trans_trip[parts[2]] = (int)trans_trip.size() + 1;
        // trips[trans_trip.size()] = Trip(trans_trip.size(), parts[0]);
        trips.push_back(Trip(trans_trip.size(), parts[0]));
        // trips.emplace(parts[2], Trip(parts[2], parts[0]));
    }

    ifstream stop_times_file(stop_times_path);
    getline(stop_times_file, line);
    while(getline(stop_times_file, line)){
        split_string(line, ',', parts);
        // Time arr(parts[1]);
        // Time dep(parts[2]);
        if(trans_stop[stoi(parts[3])] >= (int)stops.size()){
            cout << parts[3] << " " << trans_stop[stoi(parts[3])] << " " << stops.size() << "\n";
        }
        assert(trans_stop[stoi(parts[3])] < (int)stops.size());
        assert(trans_trip[parts[0]] < (int)trips.size());
        trips[trans_trip[parts[0]]].route.push_back(Vertex(stops[trans_stop[stoi(parts[3])]], Time(parts[1])));
    }
}
void Data::run_checker(){
    for(auto &stop : stops){
        assert(stop.id < stops_lim);
        assert(stop.id != -1);
    }
    int day_line_ctr = 0;
    for(auto &trip : trips){
        assert(trip.id != -1);
        day_line_ctr = 0;
        for(int i = 1; i < (int)trip.route.size(); i++){
            if(trip.route[i].time < trip.route[i - 1].time) day_line_ctr++;
        }
        assert(day_line_ctr < 2);
    }
}