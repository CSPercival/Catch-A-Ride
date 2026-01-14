#include "transit_matrix_preprocess/enhancer.hpp"

void prepare(Stops *stop_data){
    for(auto &stop : stop_data->stops){
        if(!stop.reachable.has_value()) 
            stop.reachable = vector<Stop_lite>();
        if(!stop.connections.has_value()){
            stop.connections = vector<vector<Edge_lite>>(stop_data->number_of_stops + 1);
        }
    }
}

void enhance(Stops *stop_data, Trips *trip_data){
    for(auto &trip : trip_data->trips){
        for(int i = (int)trip.route.size() -1; i >= 0; i--){
            if(trip.route[i].time < 0) break;
            Vertex_lite a = trip.route[i];
            for(int j = i + 1; j < (int)trip.route.size(); j++){
                if(2 * minutes_in_day < trip.route[j].time) break;
                Vertex_lite b = trip.route[j];
                stop_data->stops[a.stop].reachable->push_back(b.stop);
                (*(stop_data->stops[a.stop].connections))[b.stop].push_back(Edge_lite(a, b, trip.id));
            }
        }
    }
}

void polish(Stops *stop_data){
    for(auto &stop : stop_data->stops){
        sort(stop.reachable->begin(), stop.reachable->end());
        stop.reachable->erase(unique(stop.reachable->begin(), stop.reachable->end()), stop.reachable->end());
        int ptr = 0;
        for(auto &v : (*stop.connections)){
            auto tmpv = v;
            assert((v.size() != 0) ^ (find(stop.reachable->begin(), stop.reachable->end(), ptr) == stop.reachable->end()));
            ptr++;
            if(v.size() == 0) continue;
            sort(tmpv.begin(), tmpv.end());
            v.clear();
            for(auto e : tmpv){
                while(!v.empty() && e.v.time < v.back().v.time){
                    v.pop_back();
                }
                v.push_back(e);
            }
        }
    }
}

void enhance_data(Stops *stop_data, Trips *trip_data){
    prepare(stop_data);
    enhance(stop_data, trip_data);
    polish(stop_data);
}