#ifndef LITES_STRUCT
#define LITES_STRUCT

#include<string>

#include "../consts.hpp"

using namespace std;

using Stop_lite = int16_t;
using Trip_lite = int16_t;

struct Time_lite{
    int16_t em = 0;     // number of minutes elapsed since 00:00

    Time_lite() {}
    Time_lite(int in_h, int in_m){
        Time_lite(in_h * 60 + in_m);
    }
    Time_lite(int in_em){
        em = (int16_t)((in_em + minutes_in_day) % minutes_in_day);
    }
    Time_lite(string time_str){
        int h = stoi(time_str.substr(0, 2));
        int m = stoi(time_str.substr(3, 2));
        em = (int16_t)((h * 60 + m + minutes_in_day) % minutes_in_day);
        // Time_lite(h * 60 + m);
    }

    Time_lite operator+(const Time_lite &a) const{ return Time_lite(a.em + em); }
    Time_lite operator+(const int16_t &a) const{ return Time_lite(a + em); }
    Time_lite operator-(const Time_lite &a) const{ return Time_lite(em - a.em); }
    bool operator<(const Time_lite &a) const{ return em < a.em; }
    bool operator==(const Time_lite &a) const{ return em == a.em; }
    bool operator<=(const Time_lite &a) const{ return em <= a.em; }
};

struct Vertex_lite{
    Stop_lite stop;
    Time_lite time;
    Vertex_lite(){}
    Vertex_lite(Stop_lite in_s, Time_lite in_t) : stop(in_s), time(in_t) {}
    bool operator<(const Vertex_lite &a) const{
        return time < a.time || (time == a.time && stop < a.stop);
        // if(time == a.time) return stop.id < a.stop.id;
        // return time < a.time;
    }
    // bool operator==(const Vertex &a) const{
    //     return time == a.time && stop.id == a.stop.id;
    // }
};

struct Edge_lite{
    Vertex_lite u, v;
    Trip_lite trip_id;
    Edge_lite() {}
    void print(){
        cout << "(" << u.stop << ' ' << u.time.em << " -> " << v.stop << " " << v.time.em << " via " << trip_id << ")";
    }
    Edge_lite(Vertex_lite in_u, Vertex_lite in_v, Trip_lite in_trip_id) : u(in_u), v(in_v), trip_id(in_trip_id) {}
    bool operator<(const Edge_lite &a) const{
        if(u.time.em != a.u.time.em) return u.time.em < a.u.time.em;
        if(v.time.em != a.v.time.em) return v.time.em < a.v.time.em;
        return trip_id < a.trip_id;
    }  
};

#endif