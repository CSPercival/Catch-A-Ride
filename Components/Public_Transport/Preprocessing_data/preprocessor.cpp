#include <bits/stdc++.h>
#include<math.h>

#include "consts.hpp"
#include "data_reader.hpp"
#include "structs/Data.hpp"
#include "structs/Lites.hpp"
#include "structs/Stop.hpp"
#include "structs/Time.hpp"

using namespace std;

namespace{

double deg2rads(double deg){
    return deg * (M_PI / 180.0);
}

double walk_distance(Stop &a, Stop &b){
    double phia = deg2rads(stod(a.lat));
    double lama = deg2rads(stod(a.lon));
    double phib = deg2rads(stod(b.lat));
    double lamb = deg2rads(stod(b.lon));

    double dphi = phia - phib;
    double dlam = (lama - lamb) * cos((phia + phib) / 2.0);
    return Earth_radius * sqrt(dphi * dphi + dlam * dlam);
}

Time_lite dist2time(double dist){
    return Time_lite((int)round(pow(dist, 1.1) * 60.0 / walking_speed_kmph));
}

struct Comparator{
    bool operator()(Vertex_lite &a, Vertex_lite &b){
        return b < a;
    }
};

void generate_destination_list(Vertex_lite start, Data *pt_data){
    vector<Time_lite> vis(stops_lim, minutes_in_day - 1 - transfer_time);
    priority_queue<Vertex_lite, vector<Vertex_lite>, Comparator> pq;
    Vertex_lite v(start.stop, transfer_time);
    Time_lite nt;
    pq.push(v);
    vis[v.stop] = 0;
    while(!pq.empty()){
        v = pq.top();
        pq.pop();
        if(vis[v.stop] + transfer_time < v.time) continue;
        // cout << "PQ ";
        // pt_data->stops[v.stop].print_name();
        // cout << " " << v.time.em << "\n";
        // pt_data->stops[v.stop].print_all();
        // cout << "\n";
        for(auto reachable_stop_id : pt_data->stops[v.stop].reachable){
            // Time_lite debt(start.time + v.time);
            Edge_lite edge = pt_data->stops[v.stop].get_next(Time_lite(start.time + v.time), reachable_stop_id);
            if(edge.u.time < start.time + v.time){
                if(start.time <= edge.v.time) continue;
                edge.v.time.em += minutes_in_day;
            }
            // nt = pt_data->stops[v.stop].get_next(Time_lite(start.time + v.time), reachable_stop_id).v.time;
            nt = edge.v.time - start.time;
            if(nt < vis[reachable_stop_id]){
                vis[reachable_stop_id] = nt;
                // cout << "    Adding ";
                // pt_data->stops[reachable_stop_id].print_name();
                // cout << " with time " << nt.em + transfer_time << "\n";
                // cout << "       " << debt.em << " ";
                // e.print();
                // cout << "\n";
                pq.push(Vertex_lite(reachable_stop_id, nt + transfer_time));
            }
        }
        for(Stop_lite walk_stop_id = 1; walk_stop_id < stops_lim; walk_stop_id++){
            if(v.time + pt_data->walk_matrix[v.stop][walk_stop_id] - transfer_time < vis[walk_stop_id]){
                vis[walk_stop_id] = v.time + pt_data->walk_matrix[v.stop][walk_stop_id] - transfer_time;
                // cout << "    Adding walking ";
                // pt_data->stops[walk_stop_id].print_name();
                // cout << " with time " << vis[walk_stop_id].em << "\n";
                pq.push(Vertex_lite(walk_stop_id, v.time + pt_data->walk_matrix[v.stop][walk_stop_id]));
            }
        }
    }

    cout << "Destination list for: \n";
    pt_data->stops[start.stop].print_all();
    for(int i = 1; i < stops_lim; i++){
        pt_data->stops[i].print_name();
        cout << " reached in -> ";
        Time t(start.time + vis[i]);
        t.print();
        cout << "     " << vis[i].em << " " << start.time.em;
        cout << "\n";
    }
}

// void compute_graph(Graph *graph, Data *data){
//     for(auto &stop_a : data->stops){
//         for(auto &stop_b : data->stops){
//             graph->walk_matrix[stop_a.id][stop_b.id] = dist2time(walk_distance(stop_a, stop_b));
//         }
//         // for(int m = 0; m < minutes_in_day; m++){
//         //     graph->adj_list[Vertex(stop_a, Time(m))].resize(stops_lim);
//         // }
//     }
    
//     for(auto &trip : data->trips){
//         for(int i = (int)trip.route.size() - 1; i >= 0; i--){
//             for(int j = (int)trip.route.size() - 1; j > i; j--){
//                 graph->adj_list[trip.route[i]].push_back(Edge(trip.route[i], trip.route[j], trip.id));
//             }
//         }
//     }
//     cout << data->stops.size() << " " << data->trips.size() << "\n";
//     long long ctr = 0;
//     for(auto i : graph->adj_list){
//         ctr += i.second.size();
//     }
//     cout << graph->adj_list.size() << " " << ctr << "\n";
// }

void enrich_data(Data *pt_data){
    if(!pt_data->walk_matrix_computed){
        pt_data->walk_matrix.resize(stops_lim);
        for(auto &stop_a : pt_data->stops){
            pt_data->walk_matrix[stop_a.id].resize(stops_lim);
            for(auto &stop_b : pt_data->stops){
                pt_data->walk_matrix[stop_a.id][stop_b.id] = dist2time(walk_distance(stop_a, stop_b));
            }
        }
        pt_data->walk_matrix_computed = true;
    }

    for(auto &trip : pt_data->trips){
        for(int i = (int)trip.route.size() - 1; i >= 0; i--){
            for(int j = (int)trip.route.size() - 1; j > i; j--){
                // graph->adj_list[trip.route[i]].push_back(Edge(trip.route[i], trip.route[j], trip.id));
                Vertex_lite a = trip.route[i];
                Vertex_lite b = trip.route[j];
                pt_data->stops[a.stop].reachable.push_back(b.stop);
                // pt_data->stops[a.stop].connections[b.stop].push_back({b.time, trip.id});
                pt_data->stops[a.stop].connections[b.stop].push_back(Edge_lite(a, b, trip.id));
            }
        }
    }

    for(auto &stop : pt_data->stops){
        sort(stop.reachable.begin(), stop.reachable.end());
        stop.reachable.erase(unique(stop.reachable.begin(), stop.reachable.end()), stop.reachable.end());
    
        int ptr = 0;
        for(auto &v : stop.connections){
            // cerr << pt_data->stops[ptr].name << "\n";
            // if(v.size() == 0 && find(stop.reachable.begin(), stop.reachable.end(), ptr) != stop.reachable.end()){
            //     assert(false);
            // }
            // if(v.size() != 0 && find(stop.reachable.begin(), stop.reachable.end(), ptr) == stop.reachable.end()){
            //     assert(false);
            // }
            assert((v.size() != 0) ^ (find(stop.reachable.begin(), stop.reachable.end(), ptr) == stop.reachable.end()));
            sort(v.begin(), v.end());
            ptr++;
        }
    }


}

}

// struct Edge{
//     Vertex start, dest;
//     // string line_name = "";
//     int trip_id = -1;
//     // vector<pair<string,string>>
//     int em = 0;
//     Edge(){}
//     Edge(Vertex u, Vertex v, int in_trip_id) : start(u), dest(v), trip_id(in_trip_id) {
//         em = v.time.em - u.time.em;
//         if(em < 0) em += minutes_in_day;
//     }
// };

// struct Graph{
//     // map<int, Stop> stop_map;
//     // map<pair<int, Time>, Vertex> vertex_map;
//     // map<pair<int, int>, Time> walk_matrix;
//     Time walk_matrix[stops_lim][stops_lim]; 
//     map<Vertex, vector<Edge>> adj_list;
//     // map<Vertex, map<Stop, Time>> dest_list;
//     // map<Vertex, vector<M>>
// };



Data PT_data[4];
int days_id[] = {6, 8, 3, 4}; // Mon-Thu, Fri, Sat, Sun

int zlotnicka = 1671;

int main(){
    // Data data("./../Resources/GTFS/stops.txt", "./../Resources/GTFS/trips.txt", "./../Resources/GTFS/stop_times.txt");
    for(int i = 0; i < 4; i++){
        read_data("./../Resources/GTFS/stops.txt", "./../Resources/GTFS/trips.txt", "./../Resources/GTFS/stop_times.txt", &PT_data[i], days_id[i]);
        validate_data(&PT_data[i]);
        enrich_data(&PT_data[i]);
    }

    generate_destination_list(Vertex_lite(PT_data[0].o2n_stop[zlotnicka], Time_lite("08:00:00")), &PT_data[0]);
    for(int i = 0; i < stops_lim; i++){
        cout << i << " " << PT_data[0].walk_matrix[PT_data[0].o2n_stop[zlotnicka]][i].em << "\n";
    }
    // cout << "DONE?\n";
    // data.run_checker();
    // compute_graph(&graph, &data);
    // Time t;
    // Stop a = (*data.stops.begin()).second, b = (*data.stops.begin()).second;
    // for(int i = 0; i < 2337; i++){
    //     for(int j = 0; j < 2337; j++){
    //         t = dist2time(distance(a, b));
    //     }
    // }
    // for(auto stop : PT_data.stops){
    //     // printf("%d - (%d, %s, %lf, %lf)\n", stop.first, stop.second.id, stop.second.name, stop.second.lat, stop.second.lon);
    //     cout << stop.id<< " " << stop.name<< " " << stop.lat << " " << stop.lon << "\n";
    // }
    // cout << PT_data.stops.size() << "\n";
    // for(auto trip : PT_data.trips){
    //     if(rand() > 2000000) continue;
    //     cout << trip.id << " " << trip.line_name << " route: ";
    //     for(auto i : trip.route){
    //         cout << "(" << PT_data.stops[i.stop].name << "," << (int)i.time.em / 60 << ":" << (int)i.time.em % 60 << ") ";
    //     }
    //     cout << '\n';
    // }

    // int max_reach = 0;
    // for(auto stop : PT_data.stops){
    //     if(stop.id != 2314)
    //         if(rand() > 2000000) continue;
    //     stop.print();
    //     max_reach = max(max_reach, (int)stop.reachable.size());
        // cout << stop.id << " " << stop.name << " " << stop.lat << " " << stop.lon << "\n";
        // cout << "    reachable";
        // for(auto i : stop.reachable){
        //     cout << PT_data.stops[i].name << " ";
        // }
        // cout << "\n";
    // }
    // cout << max_reach << "\n";
}