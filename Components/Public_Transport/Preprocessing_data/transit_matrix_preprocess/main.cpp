#include <iostream>
#include <thread>
#include <chrono>
#include <ctime>
#include <iomanip>

#include "consts.hpp"
#include "transit_matrix_preprocess/engine.hpp"
#include "transit_matrix_preprocess/data_readers.hpp"
#include "transit_matrix_preprocess/data_writer.hpp"
#include "transit_matrix_preprocess/enhancer.hpp"
#include "shared_structs/stops.hpp"
#include "shared_structs/trips.hpp"

using namespace std;

// int zlotnicka = 1749; // 1671 -> 1749
// int psary_parkowa = 1222; // 3208 -> 1222
// int psary_wolnosci = 2324; // 5599 ->2324
// int most_grunwaldzki = 632; // 1504 -> 632

namespace{

Stops stop_data;
Trips trip_data;
vector<vector<double>> walk_matrix;

void log_time() {
    auto now = std::chrono::system_clock::now();
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);
    std::cerr << "[" << std::put_time(std::localtime(&now_time), "%Y-%m-%d %H:%M:%S") << "] ";
}

void produce_travel_matrix_part(string dir_path, string file_name, int first_id, int last_id, bool create_header){
    Destination_Lists_Writer DLW(dir_path, file_name, stop_data.number_of_stops, create_header);
    vector<Time_lite> reach_times;
    vector<pair<Stop_lite, Trip_lite>> predecessors;
    for(Stop_lite stop_it = (Stop_lite)first_id; stop_it < last_id; stop_it++){
        for(Time_lite time_it = 0; time_it < minutes_in_day; time_it++){
            compute_travel_vector(Vertex_lite(stop_it, time_it), &stop_data, &walk_matrix, reach_times, predecessors);
            DLW.write_content(reach_times, predecessors);
        }
        log_time();
        cerr << "Produced Travel Time vector for stop: " << stop_it << " (" << 100 * (stop_it - first_id + 1) / (last_id - first_id) << "%)\n"; 
    }
    DLW.destructor();
}

void produce_travel_matrix(string dir_path, string file_name, int thread_number){
    if(thread_number <= 1){
        produce_travel_matrix_part(dir_path, file_name, 1, stop_data.number_of_stops + 1, true);
    } else {
        vector<thread> workers;
        vector<string> file_names;
        int batch_size = (stop_data.number_of_stops + thread_number - 1) / thread_number;
        for(int i = 1; i <= stop_data.number_of_stops; i += batch_size){
            // cout << i << " " << min(i + batch_size, stop_data.number_of_stops + 1) << " " << to_string(i) + file_name << "\n";
            file_names.push_back(to_string(i) + file_name);
            workers.emplace_back(produce_travel_matrix_part, dir_path, to_string(i) + file_name,
                                    i, min(i + batch_size, stop_data.number_of_stops + 1), false);
        }
        for(auto & w : workers){
            w.join();
        }
        log_time();
        cerr << "Merging files\n";
        Destination_Lists_Writer DLW(dir_path, file_name, stop_data.number_of_stops, true);
        for(auto fn : file_names){
            DLW.copy_from_file(dir_path + "/" + fn);
            log_time();
            cerr << "Merged file " << fn << "\n";
        }
    }
}

}



int main(){
    string resources_path = "./../Resources/Preprocessed_Data/";
    string stops_path = resources_path + "Common/Stops.json";
    string walk_matrix_path = resources_path + "Common/Walk_Matrix.json";
    
    log_time();
    cerr << "START\n";
    read_stops(stops_path, &stop_data);
    read_walk_matrix(walk_matrix_path, &walk_matrix);

    for(int day_id = 0; day_id < 1; day_id++){
        log_time();
        cerr << "Start computing travel matrix for " << day_names[day_id] <<"\n";
        read_trips(resources_path + day_names[day_id] + "/Trips.json", &trip_data);
        log_time();
        cerr << "#1\n";
        enhance_data(&stop_data, &trip_data);
        log_time();
        cerr << "#2\n";
        produce_travel_matrix(resources_path + day_names[day_id], "Travel_Data.bin", thread::hardware_concurrency());
    }
}