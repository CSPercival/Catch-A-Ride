#ifndef LITES_STRUCT
#define LITES_STRUCT

#include<string>

#include "../consts.hpp"

using namespace std;

using Stop_lite = short;
using Trip_lite = int;

struct Time_lite{
    short em = 0;     // number of minutes elapsed since 00:00

    Time_lite() {}
    Time_lite(int in_h, int in_m){
        Time_lite(in_h * 60 + in_m);
    }
    Time_lite(int in_em){
        em = (short)((in_em + minutes_in_day) % minutes_in_day);
    }
    Time_lite(string &time_str){
        int h = stoi(time_str.substr(0, 2));
        int m = stoi(time_str.substr(3, 2));
        em = (short)((h * 60 + m + minutes_in_day) % minutes_in_day);
        // Time_lite(h * 60 + m);
    }

    Time_lite operator+(const Time_lite &a) const{ return Time_lite(a.em + em); }
    Time_lite operator-(const Time_lite &a) const{ return Time_lite(em - a.em); }
    bool operator<(const Time_lite &a) const{ return em < a.em; }
    bool operator==(const Time_lite &a) const{ return em == a.em; }
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

#endif