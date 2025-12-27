#include "Queue.hpp"


Vertex_lite Lazy_Queue::top_pop(){
    if(standard_pq.empty()){
        return top_pop_walk();
    }
    if(walk_pq.empty()){
        return top_pop_standard();
    }
    if(walk_pq.top().v <  standard_pq.top()){
        return top_pop_walk(); 
    } else {
        return top_pop_standard();
    }
}

Vertex_lite Lazy_Queue::top_pop_standard(){
    Vertex_lite ans = standard_pq.top();
    standard_pq.pop();
    // cout << "STANDARD" << endl;
    return ans;
}

Vertex_lite Lazy_Queue::top_pop_walk(){
    Walk_Record ans = walk_pq.top();
    walk_pq.pop();
    // cout << "WALKKK" << endl;
    push_walk(ans.parent, ans.ctr + 1);
    return ans.v;
}

void Lazy_Queue::push_standard(Vertex_lite a){
    standard_pq.push(a);
}

void Lazy_Queue::push_walk(Stop_lite a, int ctr){
    if(pt_data->walk_matrix_sorted[a].size() <= ctr) return;
    Vertex_lite next_walk = pt_data->walk_matrix_sorted[a][ctr];
    next_walk.time = next_walk.time + (*visited)[a];
    if(next_walk.time < (*visited)[next_walk.stop]){
        (*visited)[next_walk.stop] = next_walk.time;
        (*predecessor)[next_walk.stop] = make_pair(a, 0);
    }
    Walk_Record element;
    element.v = next_walk;
    element.parent = a;
    element.ctr = ctr;
    // cout << "ADD WALK: " << next_walk.stop << " " << next_walk.time.em << " " << ctr << endl;
    walk_pq.push(element);
}

bool Lazy_Queue::empty(){
    return standard_pq.empty() && walk_pq.empty();
}