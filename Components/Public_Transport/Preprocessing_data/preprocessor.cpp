#include <bits/stdc++.h>
#include<math.h>

#include "consts.hpp"
#include "data_reader.hpp"
#include "data_writers.hpp"
#include "structs/Data.hpp"
#include "structs/Lites.hpp"
#include "structs/Stop.hpp"

using namespace std;

// int zlotnicka = 1749; // 1671 -> 1749
// int psary_parkowa = 1222; // 3208 -> 1222
// int psary_wolnosci = 2324; // 5599 ->2324
// int most_grunwaldzki = 632; // 1504 -> 632

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
    visited.assign(stops_lim, minutes_in_day);
    predecessor.assign(stops_lim, make_pair(-1,-1));
    priority_queue<Vertex_lite, vector<Vertex_lite>, Comparator> pq;
    Vertex_lite v(start.stop, transfer_time);
    Time_lite nt;
    pq.push(v);
    visited[v.stop] = 0;
    predecessor[v.stop] = {0, -1};
    while(!pq.empty()){
        v = pq.top();
        pq.pop();
        if(visited[v.stop] + transfer_time < v.time) continue;
        for(auto reachable_stop_id : pt_data->stops[v.stop].reachable){
            Edge_lite edge = pt_data->stops[v.stop].get_next(Time_lite(start.time + v.time), reachable_stop_id);
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
            for(Stop_lite walk_stop_id = 1; walk_stop_id < stops_lim; walk_stop_id++){
                if(visited[v.stop] + pt_data->walk_matrix[v.stop][walk_stop_id] < visited[walk_stop_id]){
                    visited[walk_stop_id] = visited[v.stop] + pt_data->walk_matrix[v.stop][walk_stop_id];
                    predecessor[walk_stop_id] = {v.stop, 0};
                    pq.push(Vertex_lite(walk_stop_id, v.time + pt_data->walk_matrix[v.stop][walk_stop_id]));
                }
            }
        }
    }
}

void compute_common(Data *pt_data){
    pt_data->walk_matrix.resize(stops_lim);
    for(auto &stop_a : pt_data->stops){
        pt_data->walk_matrix[stop_a.id].resize(stops_lim);
        for(auto &stop_b : pt_data->stops){
            pt_data->walk_matrix[stop_a.id][stop_b.id] = dist2time(walk_distance(stop_a, stop_b));
        }
    }
}

void enrich_data(Data *pt_data){
    for(auto &trip : pt_data->trips){
        for(int i = (int)trip.route.size() - 1; i >= 0; i--){
            if(trip.route[i].time < 0) break;
            Vertex_lite a = trip.route[i];
            for(int j = i + 1; j < (int)trip.route.size(); j++){
                if(2 * minutes_in_day < trip.route[j].time) break;
                Vertex_lite b = trip.route[j];
                pt_data->stops[a.stop].reachable.push_back(b.stop);
                pt_data->stops[a.stop].connections[b.stop].push_back(Edge_lite(a, b, trip.id));
            }
        }
    }

    for(auto &stop : pt_data->stops){
        sort(stop.reachable.begin(), stop.reachable.end());
        stop.reachable.erase(unique(stop.reachable.begin(), stop.reachable.end()), stop.reachable.end());
    
        int ptr = 0;
        for(auto &v : stop.connections){
            auto tmpv = v;
            assert((v.size() != 0) ^ (find(stop.reachable.begin(), stop.reachable.end(), ptr) == stop.reachable.end()));
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

}

Data PT_data[7];
int day_limit = 1;

int main(){
    cerr << "START\n";
    for(int i = 0; i < day_limit; i++){
        PT_data[i].id = Day(i);
    }
    read_data("./../Resources/GTFS/stops.txt", "./../Resources/GTFS/trips.txt", "./../Resources/GTFS/stop_times.txt", PT_data);
    cerr << "#0 STAGE FINISHED\n";
    
    compute_common(&PT_data[0]);
    for(int day_id = 0; day_id < day_limit; day_id++){
        validate_data(&PT_data[day_id]);
        enrich_data(&PT_data[day_id]);
    }
    cerr << "#1 STAGE FINISHED\n";

    Stops_Data_Writer SDW("./../Resources/Preprocessed_Data/Common", "Stop_Data.bin");
    for(int stop_it = 1; stop_it < stops_lim; stop_it++){
        SDW.write_content(PT_data[0].stops[stop_it]);
    }
    SDW.destructor();

    cerr << "#2 STAGE FINISHED\n";


    for(int day_id = 0; day_id < day_limit; day_id++){
        Trips_Data_Writer TDW("./../Resources/Preprocessed_Data/" + day_names[day_id], "Trip_Data.bin", day_id);
        for(int trip_it = 1; trip_it < trips_lim[day_id]; trip_it++){
            TDW.write_content(PT_data[day_id].trips[trip_it]);
        }
        TDW.destructor();
        cerr << "#3 STAGE FINISHED\n";

        Destination_Lists_Writer DLW("./../Resources/Preprocessed_Data/" + day_names[day_id], "Schedule_Data.bin");
        vector<Time_lite> reach_times;
        vector<pair<Stop_lite, Trip_lite>> predecessors;
        for(Stop_lite stop_it = 1; stop_it < stops_lim; stop_it++){
            for(Time_lite time_it = 0; time_it < minutes_in_day; time_it++){
                generate_destination_list(Vertex_lite(stop_it, time_it), &PT_data[day_id], reach_times, predecessors);
                DLW.write_content(reach_times, predecessors);
            }
            cerr << "#4 STAGE at stop: " << stop_it << " FINISHED\n"; 
        }
        DLW.destructor();
    }

    cerr << "ALL STAGES FINISHED\n";
}