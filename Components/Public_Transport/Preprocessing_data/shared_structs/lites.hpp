#pragma once

#include<string>
#include<iostream>

using namespace std;

using Stop_lite = int16_t;
using Trip_lite = uint16_t;
using Time_lite = int16_t;

struct Vertex_lite{
    Stop_lite stop;
    Time_lite time;
    Vertex_lite(){}
    Vertex_lite(Stop_lite in_s, Time_lite in_t) : stop(in_s), time(in_t) {}
    bool operator<(const Vertex_lite &a) const{
        return time < a.time || (time == a.time && stop < a.stop);
    }
};

struct Edge_lite{
    Vertex_lite u, v;
    Trip_lite trip_id;
    Edge_lite() {}
    void print(){
        cout << "(" << u.stop << ' ' << u.time << " -> " << v.stop << " " << v.time << " via " << trip_id << ")";
    }
    Edge_lite(Vertex_lite in_u, Vertex_lite in_v, Trip_lite in_trip_id) : u(in_u), v(in_v), trip_id(in_trip_id) {}
    bool operator<(const Edge_lite &a) const{
        if(u.time != a.u.time) return u.time < a.u.time;
        if(v.time != a.v.time) return v.time < a.v.time;
        return trip_id < a.trip_id;
    }  
};