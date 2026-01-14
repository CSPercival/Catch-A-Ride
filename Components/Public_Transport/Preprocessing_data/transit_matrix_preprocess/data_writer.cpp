#include <cassert>
#include <cstring>
#include <iostream>
#include <filesystem>

#include "transit_matrix_preprocess/data_writer.hpp"

using namespace std;

void write_to_file(ofstream &file, string& data, int send_size){
    assert((int)data.size() <= send_size);

    vector<char> buffer(send_size, 0);
    memcpy(buffer.data(), data.data(), data.size());
    file.write(buffer.data(), buffer.size());
}
void write_to_file(ofstream &file, long long data, int declared_size){
    uint8_t data1;
    uint16_t data2;
    uint32_t data4;

    if(declared_size == 1){
        data1 = (uint8_t)data;
        assert((long long)data1 == data);        
        file.write(reinterpret_cast<char*>(&data1), sizeof(data1));
        return;
    }
    if(declared_size == 2){
        data2 = (uint16_t)data;
        assert((long long)data2 == data);        
        file.write(reinterpret_cast<char*>(&data2), sizeof(data2));
        return;
    }
    if(declared_size == 4){
        data4 = (uint32_t)data;
        assert((long long)data4 == data);        
        file.write(reinterpret_cast<char*>(&data4), sizeof(data4));
        return;
    }
    assert(false);
}

// DESTINATION LISTS --------------------------------------------------------------------------------------------------------------

Destination_Lists_Writer::Destination_Lists_Writer(string directory_path, string file_name, int number_of_stops){
    filesystem::create_directories(directory_path);
    file.open(directory_path + "/" + file_name, ios::binary);
    assert(file.is_open());
    write_to_file(file, number_of_stops, 2);
}
void Destination_Lists_Writer::write_content(vector<Time_lite> &reach_times, vector<pair<Stop_lite, Trip_lite>> &predecessors){
    assert(reach_times.size() == predecessors.size());
    for(int i = 1; i < (int)reach_times.size(); i++){
        write_to_file(file, reach_times[i], 2);
        write_to_file(file, predecessors[i].first, 2);
        write_to_file(file, predecessors[i].second, 2);
    }
}
void Destination_Lists_Writer::destructor(){
    file.close();
}


