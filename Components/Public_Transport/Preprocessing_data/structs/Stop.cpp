#include "Stop.hpp"
#include<assert.h>

void Stop::print_all(){
    cout << id << " " << name << " " << lat << " " << lon << "\n";
    cout << "reachable from " << name << ": ";
    for(auto i : reachable){
        cout << i << " ";
    }
    cout << "\n";
    cout << "Connections from " << name << ":\n";
    for(int i = 0; i < (int)connections.size(); i++){
        if(connections[i].empty()) continue;
        cout << i << ": ";
        for(auto j : connections[i]){
            j.print();
        }
        cout << "\n";
    }
}
void Stop::print_name(){
    cout << "( " << id << " " << name << " " << lat << " " << lon << " )";
}

Edge_lite Stop::get_next(Time_lite u_time, Stop_lite v_id){
    assert(!connections[v_id].empty());
    auto it = lower_bound(connections[v_id].begin(), connections[v_id].end(), 
        Edge_lite(Vertex_lite(id, u_time), Vertex_lite(0, 0), 0));
    if(it == connections[v_id].end()){
        it = connections[v_id].begin();
    }
    return *it;
}
