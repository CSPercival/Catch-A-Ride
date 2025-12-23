#ifndef STOP_STRUCT
#define STOP_STRUCT

#include<iostream>
#include<string>
#include<vector>

#include "Lites.hpp"

using namespace std;

struct Stop{
    int id = -1;
    string name = "NN";
    string lat = "0.0", lon = "0.0";
    vector<Stop_lite> reachable;
    vector<vector<pair<Time_lite, Trip_lite>>> connections;
    Stop() {}
    Stop(int in_id, string &in_name, string &in_lat, string &in_lon) : id(in_id), name(in_name), lat(in_lat), lon(in_lon) {
        connections.resize(stops_lim);
    }
    void print(){
        cout << id << " " << name << " " << lat << " " << lon << "\n";
        cout << "reachable from " << name << ": ";
        for(auto i : reachable){
            cout << i << " ";
        }
        cout << "\n";
        cout << "Connections from " << name << ":\n";
        for(int i = 0; i < (int)connections.size(); i++){
            cout << i << ": ";
            for(auto j : connections[i]){
                cout << "(" << j.first.em << ", " << j.second << ") ";
            }
            cout << "\n";
        }
    }
};


// struct Stop_lite{
//     int id = -1;
//     Stop_lite(){}
//     bool operator<(const Stop_lite &a) const{
//         return id < a.id;
//     }
// };

#endif