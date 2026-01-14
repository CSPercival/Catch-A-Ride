#pragma once

#include<iostream>
#include<string>
#include<cassert>
#include "./../consts.hpp"
#include <nlohmann/json.hpp>

using namespace std;

struct Day{
    int8_t id = 0;
    int8_t variant = 0;
    string name = "NN";
    Day() {}
    Day(int in_id){
        assert(abs(in_id) < 240); 
        id = (int8_t)((7 + in_id) % 7);
        variant = (int8_t)day_variants[id];
        name = day_names[id];
    }
    Day operator+(const Day &a) const{ return Day(id + a.id); }
    Day operator+(const int &a) const{ return Day(id + a); }
    Day operator-(const Day &a) const{ return Day(id - a.id); }
    Day operator-(const int &a) const{ return Day(id - a); }
    bool operator==(const int &a) const{ return id == a;}
    bool operator==(const Day &a) const{ return id == a.id;}
};

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Day,
    id,
    variant,
    name
)
