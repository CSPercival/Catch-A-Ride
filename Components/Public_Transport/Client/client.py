from Components.Public_Transport.Client.data_readers.travel_data_reader import Travel_Data_Reader
from Components.Public_Transport.Client.smart_part import find_raw_route, enhance_route, find_crucial_stops
from Components.Public_Transport.Client.area_scanner import stops_in_your_area
from Components.Public_Transport.Client.aux_functions import get_stops_coords, get_single_stop_coords
from Components.Map_Service.mapors_getters import matrix_durations, single_duration

import json
from typing import Tuple, List

Coordinate = Tuple[float, float] # (lat, lng)

class PTClient:
    def __init__(self, day_id, reasources_data_path, ors_walk_client):
        self.day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        self.stop_path = "Components/Public_Transport/Resources/Preprocessed_Data/Common/Stops.json"
        self.trip_path = "Components/Public_Transport/Resources/Preprocessed_Data/" + self.day_names[day_id] + "/Trips.json"
        self.travel_path = "Components/Public_Transport/Resources/Preprocessed_Data/" + self.day_names[day_id] + "/Travel_Data.bin"

        with open(self.stop_path, 'r') as f:
            self.stop_data = json.load(f)        
        with open(self.trip_path, 'r') as f:
            self.trip_data = json.load(f)
        self.travel_data_reader = Travel_Data_Reader(self.travel_path)
        self.ors_walk_client = ors_walk_client

    def _get_reach_time_stop(self, start_stop: int, end_stop: int, start_time: int):
        return self.travel_data_reader.read_single_travel_batch(start_stop, start_time, end_stop)[0] + start_time

    def _get_stop_struct(self, coordinate: Coordinate, name: str, arrival_time):
        stop_struct = {
            'id': 0,
            'lat': coordinate[0],
            'lng': coordinate[1],
            'name': name,
            'old_id': 0,
            'arrival_time': arrival_time
        }
        return stop_struct
    
    def _get_trip_struct(self):
        return {'id': 0, 'line_name': 'NN', 'old_id': '0', 'route': [], 'trip_type': -1}

    #Two common coordinates + start time -> full informations about the route
    def get_full_route(self, start: Coordinate, end: Coordinate, start_time: int, start_name="NN", end_name="NN") -> dict:
        route_info = self.get_reach_time(start, end, start_time)
        # print(route_info, flush=True)
        route_end_time = route_info[0]
        start_stop = route_info[1]
        end_stop = route_info[2]

        time_to_first_stop = round(single_duration(self.ors_walk_client.simple_path([start, get_single_stop_coords(start_stop, self.stop_data)])) / 60)
        # time_from_last_stop = round(single_duration(self.ors_walk_client.simple_path([get_single_stop_coords(end_stop, self.stop_data), end])) / 60)
        # print("time to first stop",time_to_first_stop)
        reach_times = self.travel_data_reader.get_travel_line(start_stop, start_time + time_to_first_stop)
        crucial_stops = find_crucial_stops(reach_times, start_stop, end_stop)
        raw_route = find_raw_route(crucial_stops, self.stop_data, self.trip_data)

        raw_route['stops'].insert(0, self._get_stop_struct(start, start_name, -time_to_first_stop))
        raw_route['trips'].insert(0, self._get_trip_struct())

        raw_route['stops'].append(self._get_stop_struct(end, end_name, route_end_time - start_time - time_to_first_stop))
        raw_route['trips'].append(self._get_trip_struct())

        # for it in range(len(raw_route['trips'])):
        #     print(raw_route['stops'][it])
        #     print(raw_route['trips'][it])
        # print(raw_route['stops'][-1])

        route = enhance_route(raw_route, self.stop_data, self.trip_data, start_time + time_to_first_stop)
        return route


    
    #Two stops_id + start time -> full informations about the route
    def get_full_route_stop(self, start_stop: int, end_stop: int, start_time: int) -> dict:
        reach_times = self.travel_data_reader.get_travel_line(start_stop, start_time)
        crucial_stops = find_crucial_stops(reach_times, start_stop, end_stop)
        # print(crucial_stops)
        raw_route = find_raw_route(crucial_stops, self.stop_data, self.trip_data)
        # for it in range(len(raw_route['trips'])):
        #     print(raw_route['stops'][it])
        #     print(raw_route['trips'][it])
        # print(raw_route['stops'][-1])
        # print(route)
        route = enhance_route(raw_route, self.stop_data, self.trip_data, start_time)
        return route

    def get_reach_time(self, start: Coordinate, end: Coordinate, start_time: int) -> List[int]:
        end_stop_ids = stops_in_your_area(end, self.stop_data)
        end_stop_walk_times = matrix_durations(self.ors_walk_client.matrix_s2d([end], get_stops_coords(end_stop_ids, self.stop_data), ['duration']))[0]
        end_stop_reach_times = self.get_reach_times(start, end_stop_ids, start_time)
        ans = [1e9, -1, -1] # duration, start stop, end stop
        for end_id, end_walk, end_reach in zip(end_stop_ids, end_stop_walk_times, end_stop_reach_times):
            if ans[0] > round(end_walk/60) + end_reach[0]:
                ans = [round(end_walk/60) + end_reach[0], end_reach[1], end_id]
        return ans

    #Common start coordinate + time -> in what time stops from end_ids list can be reached
    def get_reach_times(self, start: Coordinate, end_ids: List[int], start_time: int) -> List[List[int]]:
        # print("GET REACH TIMES")
        start_stop_ids = stops_in_your_area(start, self.stop_data)
        start_stop_times = matrix_durations(self.ors_walk_client.matrix_s2d([start], get_stops_coords(start_stop_ids, self.stop_data), ['duration']))[0]
        # print("start stop ids:", start_stop_ids)
        # print("Start stop times:", start_stop_times)
        return self.get_reach_times_stop(start_stop_ids, end_ids, [round(sst/60) + start_time for sst in start_stop_times])
    
    #In what time stops from end_ids can be reached and what was the starting point, 
    # if starting point is one of the stops from start_ids at given time
    def get_reach_times_stop(self, start_ids: List[int], end_ids: List[int], start_times: List[int]) -> List[List[int]]:
        # print("GET REACH TIMES STOP")
        # print("start ids:", start_ids) 
        # print("end ids:", end_ids)
        # print("start times:", start_times)
        final_reach_times = [[1e9, -1] for i in range(len(end_ids))]
        for id, start_time in zip(start_ids, start_times):
            single_reach_times = [travel_batch[0] + start_time for travel_batch in self.travel_data_reader.get_travel_line(id, start_time)]
            for i in range(len(end_ids)):
                if final_reach_times[i][0] > single_reach_times[end_ids[i]]:
                    final_reach_times[i] = [single_reach_times[end_ids[i]], id]
        # print("GET REACH TIMES STOP - END")
        return final_reach_times
