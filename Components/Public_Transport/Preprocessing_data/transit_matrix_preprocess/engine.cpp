
#include <queue>

#include "transit_matrix_preprocess/engine.hpp"

Time_lite dist2time(double dist){
    return Time_lite((int)round(dist * 60.0 / 1000.0 / walking_speed_kmph));
}

struct Comparator{
    bool operator()(Vertex_lite &a, Vertex_lite &b){
        return b < a;
    }
};

void compute_travel_vector(
    Vertex_lite start, Stops *stop_data, Trips *trip_data, vector<vector<double>> *walk_matrix, 
    vector<Time_lite> &visited, vector<pair<Stop_lite, Trip_lite>> &predecessor){
    int stops_limit = stop_data->number_of_stops + 1;
    visited.assign(stops_limit, minutes_in_day);
    predecessor.assign(stops_limit, make_pair(-1,-1));
    priority_queue<Vertex_lite, vector<Vertex_lite>, Comparator> pq;
    Vertex_lite v(start.stop, transfer_time);
    Time_lite nt;
    pq.push(v);
    visited[v.stop] = 0;
    predecessor[v.stop] = {0, -1};
    while(!pq.empty()){
        v = pq.top();
        pq.pop();
        // cout << "("<< v.stop << ", " << v.time << ")\n";
        if(visited[v.stop] + transfer_time < v.time) continue;
        for(auto reachable_stop_id : (*stop_data->stops[v.stop].reachable)){
            Edge_lite edge = stop_data->stops[v.stop].get_next(Time_lite(start.time + v.time), reachable_stop_id);
            nt = edge.v.time - start.time;
            assert(0 <= nt);
            assert(v.time <= nt);
            if(nt < visited[reachable_stop_id]){
                visited[reachable_stop_id] = nt;
                predecessor[reachable_stop_id] = {v.stop, edge.trip_id};
                pq.push(Vertex_lite(reachable_stop_id, nt + transfer_time));
            }
        }
        if(predecessor[v.stop].second != 0){
            for(Stop_lite walk_stop_id = 1; walk_stop_id < stops_limit; walk_stop_id++){
                Time_lite travel_time = dist2time((*walk_matrix)[v.stop][walk_stop_id]);
                if(visited[v.stop] + travel_time < visited[walk_stop_id]){
                    visited[walk_stop_id] = visited[v.stop] + travel_time;
                    predecessor[walk_stop_id] = {v.stop, 0};
                    pq.push(Vertex_lite(walk_stop_id, v.time + travel_time));
                }
            }
        }
    }
}