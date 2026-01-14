#pragma once

inline const double Earth_radius = 6371.0;
inline const double walking_speed_kmph = 5.15;
inline const int minutes_in_day = 1440;
inline const int stops_hard_lim = 3000;
inline const int transfer_time = 1;

inline const int days_num = 7;
inline const int day_variants[] = {6, 6, 6, 6, 8, 3, 4};
inline const std::string day_names[] = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
inline const std::string trip_id_endings[] = {"_0", "_1", "_2"};
inline const int time_shifts[] = {-minutes_in_day, 0, minutes_in_day};

inline int stops_lim = (int)1e9;
inline int trips_lim[] = {(int)1e9, (int)1e9, (int)1e9, (int)1e9, (int)1e9, (int)1e9, (int)1e9};

inline int stop_name_max = 1;
inline int line_name_max = 1;
inline int latitude_max = 1;
inline int longtitude_max = 1;