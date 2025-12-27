#ifndef QUEUE_STRUCT
#define QUEUE_STRUCT

#include<iostream>
#include<vector>
#include<queue>

#include "structs/Data.hpp"
#include "structs/Lites.hpp"

using namespace std;

struct Lazy_Queue{
    struct Comparator_standard{
        bool operator()(Vertex_lite &a, Vertex_lite &b){
            return b < a;
        }
    };
    struct Walk_Record{
        Vertex_lite v;
        Stop_lite parent;
        int ctr;
    };
    struct Comparator_walk{
        bool operator()(Walk_Record &a, Walk_Record &b){
            if(b.v == a.v) return b.parent < a.parent;
            return b.v < a.v;
        }
    };
    Data *pt_data;
    vector<Time_lite> *visited;
    vector<pair<Stop_lite, Trip_lite>> *predecessor;

    priority_queue<Vertex_lite, vector<Vertex_lite>, Comparator_standard> standard_pq;
    priority_queue<Walk_Record, vector<Walk_Record>, Comparator_walk> walk_pq;
    
    Lazy_Queue(Data *in_pt_data, vector<Time_lite> *in_visited, vector<pair<Stop_lite, Trip_lite>> *in_predecessor) : pt_data(in_pt_data), visited(in_visited), predecessor(in_predecessor) {}
    
    Vertex_lite top_pop();
    Vertex_lite top_pop_standard();
    Vertex_lite top_pop_walk();
    void push_standard(Vertex_lite a);
    void push_walk(Stop_lite a, int ctr);
    bool empty();
};

#endif