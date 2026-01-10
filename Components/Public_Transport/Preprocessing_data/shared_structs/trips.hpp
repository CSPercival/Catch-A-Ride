#pragma once

#include<iostream>
#include<string>

#include"lites.hpp"
#include"day.hpp"

using namespace std;

struct Trip{
    Trip_lite id = -1;
    string old_id = "0";
    string line_name = "NN";
    int trip_type = -1;     // trips start on the: 0 - day before, 1 - present day, 2 - day after
    vector<Vertex_lite> route;
    Trip() {}
    Trip(Trip_lite in_id, string &in_old_id, string &in_name, int in_trip_type) : 
        id(in_id), old_id(in_old_id), line_name(in_name), trip_type(in_trip_type) {}
    void print_name(){
        cout << " (trip " << id << ", " << line_name << ") ";
    }
    void print_all(){
        cout << "id: " << id << " name: " << line_name << "\n";
        cout << "route: ";
        for(auto i : route){
            cout << " (" << i.stop << ", " << i.time << ") ";
        }
        cout << "\n";
    }
};

struct Trips{
    int number_of_trips;
    Day day;
    map<string, Trip_lite> id_mapping;
    map<string, vector<Trip_lite>> line_name_mapping;
    vector<Trip> trips;
};
