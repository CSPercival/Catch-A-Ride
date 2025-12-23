#ifndef STRUCTS
#define STRUCTS

#include<bits/stdc++.h>
#include<math.h>
#include"consts.hpp"

using namespace std;

namespace{

void hm2em(int h, int m, int *em){
    (*em) = h * 60 + m;    
}
void em2hm(int em, int *h, int *m){
    (*h) = em / 60;
    (*m) = em % 60;
}

double deg2rads(double deg){
    return deg * (M_PI / 180.0);
}

}

struct Time{
    int h = 0, m = 0;
    int em = 0;     // number of minutes elapsed since 00:00
    
    Time() {}
    Time(int in_h, int in_m) : h(in_h), m(in_m){
        h += m / 60;
        h %= 24;
        m %= 60;
        hm2em(h, m, &em);
    }
    Time(int in_em) : em(in_em){
        em = (em + minutes_in_day) % minutes_in_day;
        em2hm(em, &h, &m);
    }
    Time(string &time){
        h = stoi(time.substr(0, 2)) % 24;
        m = stoi(time.substr(3, 2));
        hm2em(h, m, &em);
    }

    Time operator+(const Time &a) const{
        return Time(a.em + em);
    }
    Time operator-(const Time &a) const{
        return Time(em - a.em);
    }
    bool operator<(const Time &a) const{
        return em < a.em;
    }
    bool operator==(const Time &a) const{
        return em == a.em;
    }
};

struct Stop{
    int id = -1;
    string name = "NN";
    string lat = "0.0", lon = "0.0";
    Stop() {}
    Stop(int in_id, string &in_name, string &in_lat, string &in_lon) : id(in_id), name(in_name), lat(in_lat), lon(in_lon) {}
};

struct Vertex{
    Stop stop;
    Time time;
    Vertex(){}
    Vertex(Stop in_s, Time in_t) : stop(in_s), time(in_t) {}
    bool operator<(const Vertex &a) const{
        if(time == a.time) return stop.id < a.stop.id;
        return time < a.time;
    }
    bool operator==(const Vertex &a) const{
        return time == a.time && stop.id == a.stop.id;
    }
};

struct Trip{
    int id = -1;
    string line_name = "NN";
    vector<Vertex> route;
    Trip() {}
    Trip(int in_id, string &in_name) : id(in_id), line_name(in_name) {}
};

struct Edge{
    Vertex start, dest;
    // string line_name = "";
    int trip_id = -1;
    // vector<pair<string,string>>
    int em = 0;
    Edge(){}
    Edge(Vertex u, Vertex v, int in_trip_id) : start(u), dest(v), trip_id(in_trip_id) {
        em = v.time.em - u.time.em;
        if(em < 0) em += minutes_in_day;
    }
};

struct Graph{
    // map<int, Stop> stop_map;
    // map<pair<int, Time>, Vertex> vertex_map;
    // map<pair<int, int>, Time> walk_matrix;
    Time walk_matrix[stops_lim][stops_lim]; 
    map<Vertex, vector<Edge>> adj_list;
    // map<Vertex, map<Stop, Time>> dest_list;
    // map<Vertex, vector<M>>
};

#endif