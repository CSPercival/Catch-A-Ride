from Components.Public_Transport.Client.data_readers.travel_data_reader import Travel_Data_Reader
from Components.Public_Transport.Client.smart_part import find_raw_route, enhance_route, find_crucial_stops
import json
from typing import Tuple, List

Coordinate = Tuple[float, float] # (lat, lng)

class PTClient:
    def __init__(self, day_id, reasources_data_path):
        self.day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        self.stop_path = "Components/Public_Transport/Resources/Preprocessed_Data/Common/Stops.json"
        self.trip_path = "Components/Public_Transport/Resources/Preprocessed_Data/" + self.day_names[day_id] + "/Trips.json"
        self.travel_path = "Components/Public_Transport/Resources/Preprocessed_Data/" + self.day_names[day_id] + "/Travel_Data.bin"

        with open(self.stop_path, 'r') as f:
            self.stop_data = json.load(f)
        
        # print(self.stop_data)
        # print(self.stop_data['id_mapping'])
        with open(self.trip_path, 'r') as f:
            self.trip_data = json.load(f)
        # self.travel_header.update(read_schedule_data_header(self.travel_path))
        self.tdr = Travel_Data_Reader(self.travel_path)

    def _get_reach_time_stop(self, start_stop: int, end_stop: int, start_time: int):
        pass

    #Two common coordinates + start time -> full informations about the route
    def get_full_route(self, start: Coordinate, end: Coordinate, start_time: int) -> dict:
        pass
    
    #Two stops_id + start time -> full informations about the route
    def get_full_route_stop(self, start_stop: int, end_stop: int, start_time: int) -> dict:
        reach_times = self.tdr.get_travel_line(start_stop, start_time)
        # print(reach_times)
        crucial_stops = find_crucial_stops(reach_times, start_stop, end_stop)
        print(crucial_stops)
        route = find_raw_route(crucial_stops, self.stop_data, self.trip_data)
        # print(route)
        
        # for it in range(len(route['trips'])):
        #     print(route['stops'][it])
        #     print(route['trips'][it])
        # print(route['stops'][-1])
        # print(route)
        route = enhance_route(route, self.stop_data, self.trip_data, start_time)
        # print("--------------------------------------------------------------")
        # print(json.dumps(route, indent=2))
        return route

    def get_reach_time(self, start: Coordinate, end: Coordinate, start_time: int) -> int:
        pass

    #Common start coordinate + time -> in what time stops from end_ids list can be reached
    def get_reach_times(self, start: Coordinate, end_ids: List[int], start_time: int) -> dict:
        pass
    
    #In what time stops from end_ids can be reached if starting point is one of the stops from start_ids at given time
    def get_reach_times_stop(self, start_ids: List[int], end_ids: List[int], start_times: List[int]) -> dict:
        final_reach_times = [1e9 for i in range(len(end_ids))]
        for id, start_time in zip(start_ids, start_times):
            single_reach_times = self.tdr.get_travel_line(id, start_time)
            for final_time, end_id in zip(final_reach_times, end_ids):
                final_time = max(final_time, single_reach_times[end_id])
        return final_reach_times
