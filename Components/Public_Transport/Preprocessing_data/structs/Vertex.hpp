#ifndef VERTEX_STRUCT
#define VERTEX_STRUCT

#include<iostream>
#include<string>

#include"Time.hpp"
#include"Stop.hpp"

using namespace std;

struct Vertex{
    Stop stop;
    Time time;
    Vertex(){}
    Vertex(Stop in_s, Time in_t) : stop(in_s), time(in_t) {}
    bool operator<(const Vertex &a) const{
        return time < a.time || (time == a.time && stop.id < a.stop.id);
        // if(time == a.time) return stop.id < a.stop.id;
        // return time < a.time;
    }
    // bool operator==(const Vertex &a) const{
    //     return time == a.time && stop.id == a.stop.id;
    // }
};



#endif