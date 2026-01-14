#include "stops.hpp"
#include "../consts.hpp"
#include<assert.h>

void Stop::print_all(){
    cout << id << " " << name << " " << lat << " " << lng << "\n";
    cout << "reachable from " << name << ": ";
    for(auto i : reachable.value()){
        cout << i << " ";
    }
    cout << "\n";
    cout << "Connections from " << name << ":\n";
    for(int i = 0; i < (int)connections.value().size(); i++){
        if(connections.value()[i].empty()) continue;
        cout << i << ": ";
        for(auto j : connections.value()[i]){
            j.print();
        }
        cout << "\n";
    }
}
void Stop::print_name(){
    cout << "( " << id << " " << name << " " << lat << " " << lng << " )";
}

Edge_lite Stop::get_next(Time_lite u_time, Stop_lite v_id){
    assert(!connections.value()[v_id].empty());
    auto it = lower_bound(connections.value()[v_id].begin(), connections.value()[v_id].end(), 
        Edge_lite(Vertex_lite(id, u_time), Vertex_lite(0, 0), 0));
    if(it == connections.value()[v_id].end()){
        return Edge_lite(Vertex_lite(id, u_time), Vertex_lite(v_id, minutes_in_day * 7), 0);
    }
    return *it;
}
