#include <bits/stdc++.h>
#include "structs.hpp"
#include "data_reader.hpp"
#include "consts.hpp"

using namespace std;

namespace{

double walk_distance(Stop &a, Stop &b){
    double phia = deg2rads(stod(a.lat));
    double lama = deg2rads(stod(a.lon));
    double phib = deg2rads(stod(b.lat));
    double lamb = deg2rads(stod(b.lon));

    double dphi = phia - phib;
    double dlam = (lama - lamb) * cos((phia + phib) / 2.0);
    return Earth_radius * sqrt(dphi * dphi + dlam * dlam);
}

Time dist2time(double dist){
    return Time(round(pow(dist, 1.1) * 60.0 / walking_speed_kmph));
}

void generate_destination_list(Vertex &start){
    vector<Time> vis(stops_lim);
    int ctr = 0;
    set<Vertex> potencials;
    queue<Vertex> wait_stops;
    pq.push(start);
}

void compute_graph(Graph *graph, Data *data){
    for(auto &stop_a : data->stops){
        for(auto &stop_b : data->stops){
            graph->walk_matrix[stop_a.id][stop_b.id] = dist2time(walk_distance(stop_a, stop_b));
        }
        // for(int m = 0; m < minutes_in_day; m++){
        //     graph->adj_list[Vertex(stop_a, Time(m))].resize(stops_lim);
        // }
    }
    
    for(auto &trip : data->trips){
        for(int i = (int)trip.route.size() - 1; i >= 0; i--){
            for(int j = (int)trip.route.size() - 1; j > i; j--){
                graph->adj_list[trip.route[i]].push_back(Edge(trip.route[i], trip.route[j], trip.id));
            }
        }
    }
    cout << data->stops.size() << " " << data->trips.size() << "\n";
    long long ctr = 0;
    for(auto i : graph->adj_list){
        ctr += i.second.size();
    }
    cout << graph->adj_list.size() << " " << ctr << "\n";
}

}

Graph graph;

int main(){
    Data data("./../../../Resources/GTFS/stops.txt", "./../../../Resources/GTFS/trips.txt", "./../../../Resources/GTFS/stop_times.txt");
    data.run_checker();
    compute_graph(&graph, &data);
    // Time t;
    // Stop a = (*data.stops.begin()).second, b = (*data.stops.begin()).second;
    // for(int i = 0; i < 2337; i++){
    //     for(int j = 0; j < 2337; j++){
    //         t = dist2time(distance(a, b));
    //     }
    // }

    // for(auto stop : data.stops){
    //     // printf("%d - (%d, %s, %lf, %lf)\n", stop.first, stop.second.id, stop.second.name, stop.second.lat, stop.second.lon);
    //     cout << stop.first<< " " << stop.second.id<< " " << stop.second.name<< " " << stop.second.lat << " " << stop.second.lon << "\n";
    // }

}