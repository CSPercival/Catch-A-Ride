#include <iostream>

#include "consts.hpp"
#include "computing_travel_matrix/computer.hpp"
#include "computing_travel_matrix/data_readers.hpp"
#include "computing_travel_matrix/data_writer.hpp"
#include "computing_travel_matrix/enhancer.hpp"
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
// , Stops *stop_data, Trips *trip_data, *vector<vector<double>> walk_matrix
void produce_travel_matrix_part(string dir_path, string file_name, int first_id, int last_id){
    Destination_Lists_Writer DLW(dir_path, file_name, stop_data.number_of_stops);
    vector<Time_lite> reach_times;
    vector<pair<Stop_lite, Trip_lite>> predecessors;
    for(Stop_lite stop_it = first_id; stop_it < last_id; stop_it++){
        for(Time_lite time_it = 0; time_it < minutes_in_day; time_it++){
            cerr << stop_it << "  -  " << time_it << "\n";
            compute_travel_vector(Vertex_lite(stop_it, time_it), &stop_data, &trip_data, &walk_matrix, reach_times, predecessors);
            DLW.write_content(reach_times, predecessors);
        }
        cerr << "Produced Travel Time vector for stop: " << stop_it << " (" << 100 * (stop_it - first_id + 1) / (last_id - first_id) << "%)\n"; 
    }
    DLW.destructor();
}

void produce_travel_matrix(string dir_path, string file_name){
    produce_travel_matrix_part(dir_path, file_name, 1, stop_data.number_of_stops + 1);
}

}



int main(){
    string resources_path = "./../Resources/Preprocessed_Data/";
    string stops_path = resources_path + "Common/Stops.json";
    string walk_matrix_path = resources_path + "Common/Walk_Matrix.json";
    // string stop_times_path = resources_path + "GTFS/stop_times.txt";
    
    cerr << "START\n";
    read_stops(stops_path, &stop_data);
    read_walk_matrix(walk_matrix_path, &walk_matrix);

    for(int day_id = 0; day_id < days_num; day_id++){
        cerr << "Start computing travel matrix for " << day_names[day_id] <<"\n";
        read_trips(resources_path + day_names[day_id] + "/Trips.json", &trip_data);
        cerr << "#1\n";
        enhance_data(&stop_data, &trip_data);
        cerr << "#2\n";
        produce_travel_matrix(resources_path + day_names[day_id], "Travel_Data.bin");
        // compute_travel_matrix(&stop_data, &trip_data, &walk_matrix);
    }



    // for(int i = 0; i < day_limit; i++){
    //     PT_data[i].id = Day(i);
    // }
    // read_data("./../Resources/GTFS/stops.txt", "./../Resources/GTFS/trips.txt", "./../Resources/GTFS/stop_times.txt", PT_data);
    // cerr << "#0 STAGE FINISHED\n";
    
    // compute_common(&PT_data[0]);
    // for(int day_id = 0; day_id < day_limit; day_id++){
    //     validate_data(&PT_data[day_id]);
    //     enrich_data(&PT_data[day_id]);
    // }
    // cerr << "#1 STAGE FINISHED\n";

    // Stops_Data_Writer SDW("./../Resources/Preprocessed_Data/Common", "Stop_Data.bin");
    // for(int stop_it = 1; stop_it < stops_lim; stop_it++){
    //     SDW.write_content(PT_data[0].stops[stop_it]);
    // }
    // SDW.destructor();

    // cerr << "#2 STAGE FINISHED\n";


    // for(int day_id = 0; day_id < day_limit; day_id++){
    //     Trips_Data_Writer TDW("./../Resources/Preprocessed_Data/" + day_names[day_id], "Trip_Data.bin", day_id);
    //     for(int trip_it = 1; trip_it < trips_lim[day_id]; trip_it++){
    //         TDW.write_content(PT_data[day_id].trips[trip_it]);
    //     }
    //     TDW.destructor();
    //     cerr << "#3 STAGE FINISHED\n";

    //     Destination_Lists_Writer DLW("./../Resources/Preprocessed_Data/" + day_names[day_id], "Schedule_Data.bin");
    //     vector<Time_lite> reach_times;
    //     vector<pair<Stop_lite, Trip_lite>> predecessors;
    //     for(Stop_lite stop_it = 1; stop_it < stops_lim; stop_it++){
    //         for(Time_lite time_it = 0; time_it < minutes_in_day; time_it++){
    //             generate_destination_list(Vertex_lite(stop_it, time_it), &PT_data[day_id], reach_times, predecessors);
    //             DLW.write_content(reach_times, predecessors);
    //         }
    //         cerr << "#4 STAGE at stop: " << stop_it << " FINISHED\n"; 
    //     }
    //     DLW.destructor();
    // }

    // cerr << "ALL STAGES FINISHED\n";
}