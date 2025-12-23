#ifndef TIME_STRUCT
#define TIME_STRUCT

#include<iostream>
#include<string>
#include"./../consts.hpp"

struct Time{
    int h = 0, m = 0;
    int em = 0;     // number of minutes elapsed since 00:00
    
    void hm2em(int th, int tm, int *tem){ (*tem) = th * 60 + tm; }
    void em2hm(int tem, int *th, int *tm){
        (*th) = tem / 60;
        (*tm) = tem % 60;
    }

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

    Time operator+(const Time &a) const{ return Time(a.em + em); }
    Time operator-(const Time &a) const{ return Time(em - a.em); }
    bool operator<(const Time &a) const{ return em < a.em; }
    bool operator==(const Time &a) const{ return em == a.em; }
};



#endif