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

void write_to_file_vc(ofstream &file, vector<char>& data, int send_size){
    assert((int)data.size() == send_size);
    file.write(data.data(), data.size());
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

void write_to_buffer(char **ptr, long long data, int declared_size){
    uint8_t data1;
    uint16_t data2;
    uint32_t data4;

    if(declared_size == 1){
        data1 = (uint8_t)data;
        assert((long long)data1 == data);        
        // file.write(reinterpret_cast<char*>(&data1), sizeof(data1));
        memcpy((*ptr), &data1, sizeof(data1));
        (*ptr) += sizeof(data1);
        return;
    }
    if(declared_size == 2){
        data2 = (uint16_t)data;
        assert((long long)data2 == data);        
        // file.write(reinterpret_cast<char*>(&data2), sizeof(data2));
        memcpy((*ptr), &data2, sizeof(data2));
        (*ptr) += sizeof(data2);
        return;
    }
    if(declared_size == 4){
        data4 = (uint32_t)data;
        assert((long long)data4 == data);        
        // file.write(reinterpret_cast<char*>(&data4), sizeof(data4));
        memcpy((*ptr), &data4, sizeof(data4));
        (*ptr) += sizeof(data4);
        return;
    }
    assert(false);
}

// DESTINATION LISTS --------------------------------------------------------------------------------------------------------------

Destination_Lists_Writer::Destination_Lists_Writer(string directory_path, string file_name, int number_of_stops, bool create_header){
    filesystem::create_directories(directory_path);
    file.open(directory_path + "/" + file_name, ios::binary);
    assert(file.is_open());
    buffer.resize(number_of_stops * 6);
    if(create_header){
        write_to_file(file, number_of_stops, 2);
    }
}

void Destination_Lists_Writer::write_content(vector<Time_lite> &reach_times, vector<pair<Stop_lite, Trip_lite>> &predecessors){
    assert(reach_times.size() == predecessors.size());
    char* ptr = buffer.data();
    for(int i = 1; i < (int)reach_times.size(); i++){
        write_to_buffer(&ptr, reach_times[i], 2);
        write_to_buffer(&ptr, predecessors[i].first, 2);
        write_to_buffer(&ptr, predecessors[i].second, 2);
    }
    write_to_file_vc(file, buffer, ((int)reach_times.size() - 1) * 6);
}

void Destination_Lists_Writer::copy_from_file(string file_path){
    ifstream file_to_copy(file_path, std::ios::binary);
    file << file_to_copy.rdbuf(); 
    file_to_copy.close();
    remove(file_path.c_str());
}

void Destination_Lists_Writer::destructor(){
    file.close();
}


