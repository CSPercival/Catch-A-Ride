#include <bits/stdc++.h>
#include<math.h>

#include "consts.hpp"
#include "data_reader.hpp"
#include "data_writers.hpp"
#include "structs/Data.hpp"
#include "structs/Lites.hpp"
#include "structs/Stop.hpp"
#include "structs/Time.hpp"
#include "structs/Queue.hpp"

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

void generate_destination_list(Vertex_lite start, Data *pt_data, vector<Time_lite> &visited, vector<pair<Stop_lite, Trip_lite>> &predecessor){
    visited.assign(stops_lim, minutes_in_day - 1 - transfer_time);
    vector<int> dead(stops_lim, 0);
    int dead_ctr = 1;
    predecessor.assign(stops_lim, make_pair(-1,-1));
    // priority_queue<Vertex_lite, vector<Vertex_lite>, Comparator> pq;
    Lazy_Queue pq(pt_data, &visited, &predecessor);
    Vertex_lite v(start.stop, transfer_time);
    Time_lite nt;
    pq.push_standard(v);
    visited[v.stop] = 0;
    dead[v.stop] = 0;
    while(!pq.empty() && dead_ctr < stops_lim){
        v = pq.top_pop();
        if(dead[v.stop]) continue;
        dead[v.stop] = 1;
        dead_ctr++;
        // if(!(visited[v.stop] == minutes_in_day - 1 - transfer_time)) continue;
        // cout << "PQ ";
        // pt_data->stops[v.stop].print_name();
        // cout << " " << v.time.em << endl;
        
        // pt_data->stops[v.stop].print_all();
        // cout << endl;
        for(auto reachable_stop_id : pt_data->stops[v.stop].reachable){
            // Time_lite debt(start.time + v.time);
            Edge_lite edge = pt_data->stops[v.stop].get_next(Time_lite(start.time + v.time), reachable_stop_id);
            if(edge.u.time < start.time + v.time){
                if(start.time <= edge.v.time) continue;
                edge.v.time.em += minutes_in_day;
            }
            // nt = pt_data->stops[v.stop].get_next(Time_lite(start.time + v.time), reachable_stop_id).v.time;
            nt = edge.v.time - start.time;
            if(nt < visited[reachable_stop_id]){
                visited[reachable_stop_id] = nt;
                predecessor[reachable_stop_id] = {v.stop, edge.trip_id};
                // cout << "    Adding ";
                // pt_data->stops[reachable_stop_id].print_name();
                // cout << " with time " << nt.em + transfer_time << "\n";
                // cout << "       " << debt.em << " ";
                // e.print();
                // cout << "\n";
                pq.push_standard(Vertex_lite(reachable_stop_id, nt + transfer_time));
            }
        }
        /*TODO - lazy way of adding walking destinations to the queue*/
        if(predecessor[v.stop].second != 0){
            pq.push_walk(v.stop, 1);
            // for(Stop_lite walk_stop_id = 1; walk_stop_id < stops_lim; walk_stop_id++){
            //     if(v.time + pt_data->walk_matrix[v.stop][walk_stop_id] - transfer_time < visited[walk_stop_id]){
            //         visited[walk_stop_id] = v.time + pt_data->walk_matrix[v.stop][walk_stop_id] - transfer_time;
            //         predecessor[walk_stop_id] = {v.stop, 0};
            //         // cout << "    Adding walking ";
            //         // pt_data->stops[walk_stop_id].print_name();
            //         // cout << " with time " << visited[walk_stop_id].em << "\n";
            //         pq.push(Vertex_lite(walk_stop_id, v.time + pt_data->walk_matrix[v.stop][walk_stop_id]));
            //     }
            // }
        }
        // for(int sorted_walk_stop_id = 1; sorted_walk_stop_id < stops_lim /*&&
        //     pt_data->walk_matrix_sorted[v.stop][sorted_walk_stop_id].time <= 30*/; sorted_walk_stop_id++){
        //     Time_lite walk_time = pt_data->walk_matrix_sorted[v.stop][sorted_walk_stop_id].time;
        //     Stop_lite walk_dest = pt_data->walk_matrix_sorted[v.stop][sorted_walk_stop_id].stop;
        //     if(v.time + walk_time - transfer_time < visited[walk_dest]){
        //         visited[walk_dest] = v.time + walk_time - transfer_time;
        //         predecessor[walk_dest] = {v.stop, 0};
        //         // cout << "    Adding walking ";
        //         // pt_data->stops[walk_stop_id].print_name();
        //         // cout << " with time " << visited[walk_stop_id].em << "\n";
        //         pq.push(Vertex_lite(walk_dest, v.time + walk_time));
        //     }
        // }
    }
    cerr << "DONE" << start.stop << "\n";
    // for(int i = 1; i < stops_lim; i++){
    //     max_em = max(max_em, (int)visited[i].em);
    // }
    // cout << "Destination list for: \n";
    // pt_data->stops[start.stop].print_all();
    // for(int i = 1; i < stops_lim; i++){
    //     pt_data->stops[i].print_name();
    //     cout << " reached in -> ";
    //     Time t(start.time + visited[i]);
    //     t.print();
    //     cout << "     " << visited[i].em << " " << start.time.em;
    //     cout << "\n";
    // }
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
        pt_data->walk_matrix_sorted.resize(stops_lim);
        for(auto &stop_a : pt_data->stops){
            pt_data->walk_matrix[stop_a.id].resize(stops_lim);
            pt_data->walk_matrix_sorted[stop_a.id].resize(stops_lim);
            for(auto &stop_b : pt_data->stops){
                pt_data->walk_matrix[stop_a.id][stop_b.id] = dist2time(walk_distance(stop_a, stop_b));
                pt_data->walk_matrix_sorted[stop_a.id][stop_b.id] = Vertex_lite((Stop_lite)stop_b.id, pt_data->walk_matrix[stop_a.id][stop_b.id]);
            }
            sort(pt_data->walk_matrix_sorted[stop_a.id].begin() + 1, pt_data->walk_matrix_sorted[stop_a.id].end());
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
                pt_data->stops[a.stop].connections[b.stop].push_back(Edge_lite(a, b, (Trip_lite)trip.id));
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
            /*TODO - remove connections that departure earlier but arrive later*/
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
string days_names[] = {"Mon-Thu", "Fri", "Sat", "Sun"};
int day_lims = 1;
int zlotnicka = 1671;

int main(){
    // Data data("./../Resources/GTFS/stops.txt", "./../Resources/GTFS/trips.txt", "./../Resources/GTFS/stop_times.txt");
    cerr << "START\n";
    for(int i = 0; i < day_lims; i++){
        read_data("./../Resources/GTFS/stops.txt", "./../Resources/GTFS/trips.txt", "./../Resources/GTFS/stop_times.txt", &PT_data[i], days_id[i]);
        validate_data(&PT_data[i]);
        enrich_data(&PT_data[i]);
    }
    cerr << "#1 STAGE FINISHED\n";
    Stop_lite zlotnicka_id = PT_data[0].o2n_stop[zlotnicka];


    // PT_data[0].stops[zlotnicka_id].print_name();
    // for(auto i : PT_data[0].walk_matrix_sorted[zlotnicka_id]){
    //     cout << i.time.em << " to ";
    //     PT_data[0].stops[i.stop].print_name();
    //     cout << "\n";
    // }

    // int max_reach = 0;
    // int max_id = 0;
    // int sum_reach = 0;
    // vector<pair<int,int>> max_reach;
    // for(int i = 0; i < stops_lim; i++){
    //     // if(max_reach < PT_data[0].stops[i].reachable.size()){
    //     //     max_reach = PT_data[0].stops[i].reachable.size();
    //     //     max_id = i;
    //     // }
    //     max_reach.push_back({PT_data[0].stops[i].reachable.size(), i});
    //     sum_reach += max_reach.back().first;
    // }
    // sort(max_reach.begin(), max_reach.end());
    // for(int i = 0; i < max_reach.size(); i++){
    //     cout << max_reach[i].first << " ";
    //     PT_data[0].stops[max_reach[i].second].print_name();
    //     cout << "\n";
    //     // cout << max_reach[max_reach.size() - 1 - i].first << " ";
    //     // PT_data[0].stops[max_reach[max_reach.size() - 1 - i].second].print_name();
    //     // cout << "\n";
    // }
    // cout << sum_reach << "\n";
    
    Stops_Data_Writer SDW("./../Resources/Preprocessed_Data/Common", "Stop_Data.bin");
    for(int stop_it = 1; stop_it < 13; stop_it++){
        SDW.write_content(PT_data[0].stops[stop_it]);
    }
    SDW.destructor();

    cerr << "#2 STAGE FINISHED\n";


    for(int i = 0; i < day_lims; i++){
        Trips_Data_Writer TDW("./../Resources/Preprocessed_Data/" + days_names[i], "Trip_Data.bin");
        for(int trip_it = 1; trip_it < 23; trip_it++){
            TDW.write_content(PT_data[i].trips[trip_it]);
        }
        TDW.destructor();

        Destination_Lists_Writer DLW("./../Resources/Preprocessed_Data/" + days_names[i], "Dest_Data.bin");
        vector<Time_lite> reach_times;
        vector<pair<Stop_lite, Trip_lite>> predecessors;
        for(int stop_it = 0; stop_it < stops_lim; stop_it++){
            for(int time_it = 480; time_it < 481; time_it++){
                generate_destination_list(Vertex_lite((Stop_lite)stop_it, time_it), &PT_data[i], reach_times, predecessors);
                DLW.write_content(reach_times, predecessors);
            }
        }
        DLW.destructor();
    }

    cerr << "ALL STAGES FINISHED\n";
    // cerr << max_em << "\n";
    // cerr << ctr_walk << " " << ctr_walk_good << "\n";


    // generate_destination_list(Vertex_lite(PT_data[0].o2n_stop[zlotnicka], Time_lite("08:00:00")), &PT_data[0]);
    // for(int i = 0; i < stops_lim; i++){
    //     cout << i << " " << PT_data[0].walk_matrix[PT_data[0].o2n_stop[zlotnicka]][i].em << "\n";
    // }
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