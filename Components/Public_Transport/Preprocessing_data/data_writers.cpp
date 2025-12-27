#include "data_writers.hpp"

#include <cassert>
#include <cstring>
#include <iostream>
#include <filesystem>
using namespace std;

void write_to_file(ofstream &file, string& data, int send_size){
    assert((int)data.size() <= send_size);

    vector<char> buffer(send_size, 0);
    memcpy(buffer.data(), data.data(), data.size());
    file.write(buffer.data(), buffer.size());
}
void write_to_file(ofstream &file, long long data, int declared_size){
    int8_t data1;
    int16_t data2;
    int32_t data4;

    if(declared_size == 1){
        data1 = (int8_t)data;
        assert((long long)data1 == data);        
        file.write(reinterpret_cast<char*>(&data1), sizeof(data1));
        return;
    }
    if(declared_size == 2){
        data2 = (int16_t)data;
        assert((long long)data2 == data);        
        file.write(reinterpret_cast<char*>(&data2), sizeof(data2));
        return;
    }
    if(declared_size == 4){
        data4 = (int32_t)data;
        assert((long long)data4 == data);        
        file.write(reinterpret_cast<char*>(&data4), sizeof(data4));
        return;
    }
    assert(false);
}
// void write_to_file(ofstream file, long double data, int declared_size, int send_size){

// }


// DESTINATION LISTS --------------------------------------------------------------------------------------------------------------

Destination_Lists_Writer::Destination_Lists_Writer(string directory_path, string file_name){
    filesystem::create_directories(directory_path);
    file.open(directory_path + "/" + file_name, ios::binary);
    assert(file.is_open());
    write_to_file(file, stops_lim, 2);
    // int16_t number_of_stops = (int16_t)stops_lim;
    // file.write(reinterpret_cast<char*>(&number_of_stops), sizeof(number_of_stops));
}
void Destination_Lists_Writer::write_content(vector<Time_lite> &reach_times, vector<pair<Stop_lite, Trip_lite>> &predecessors){
    assert(reach_times.size() == predecessors.size());
    for(int i = 1; i < reach_times.size(); i++){
        write_to_file(file, reach_times[i].em, 2);
        write_to_file(file, predecessors[i].first, 2);
        write_to_file(file, predecessors[i].second, 2);
        // assert(sizeof(reach_times[i].em) == 2);
        // assert(sizeof(predecessors[i].first) == 2);
        // assert(sizeof(predecessors[i].second) == 2);
        // file.write(reinterpret_cast<char*>(&reach_times[i].em), sizeof(reach_times[i].em));
        // file.write(reinterpret_cast<char*>(&predecessors[i].first), sizeof(predecessors[i].first));
        // file.write(reinterpret_cast<char*>(&predecessors[i].second), sizeof(predecessors[i].second));
    }
}
void Destination_Lists_Writer::destructor(){
    file.close();
}


// STOP DATA --------------------------------------------------------------------------------------------------------------

Stops_Data_Writer::Stops_Data_Writer(string directory_path, string file_name){
    filesystem::create_directories(directory_path);
    file.open(directory_path + "/" + file_name, ios::binary);
    assert(file.is_open());
    write_to_file(file, stops_lim, 2);
    write_to_file(file, stop_name_max, 1);
    write_to_file(file, latitude_max, 1);
    write_to_file(file, longtitude_max, 1);
}
void Stops_Data_Writer::write_content(Stop &stop){
    // int16_t data_to_send = (uint16_t)stop.id;
    // assert((int)data_to_send == stop.id);
    // file.write(reinterpret_cast<char*>(&data_to_send), data_size);
    write_to_file(file, stop.id, 2);
    write_to_file(file, stop.name, stop_name_max);
    write_to_file(file, stop.lat, latitude_max);
    write_to_file(file, stop.lon, longtitude_max);

}
void Stops_Data_Writer::destructor(){
    file.close();
}


// TRIP DATA --------------------------------------------------------------------------------------------------------------

Trips_Data_Writer::Trips_Data_Writer(string directory_path, string file_name){
    filesystem::create_directories(directory_path);
    file.open(directory_path + "/" + file_name, ios::binary);
    assert(file.is_open());
    write_to_file(file, trips_lim, 2);
    write_to_file(file, line_name_max, 1);
}
void Trips_Data_Writer::write_content(Trip &trip){
    write_to_file(file, trip.id, 2);
    write_to_file(file, trip.line_name, line_name_max);
}
void Trips_Data_Writer::destructor(){
    file.close();
}

