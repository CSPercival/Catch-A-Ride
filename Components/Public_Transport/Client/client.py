from Components.Public_Transport.Client.data_readers.travel_data_reader import Travel_Data_Reader
from Components.Public_Transport.Client.smart_part import find_raw_route, enhance_route
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

    def _get_reach_time(self, start_stop: int, end_stop: int, start_time: int):
        pass

    #Two common coordinates + start time -> full informations about the route
    def get_full_route(self, start: Coordinate, end: Coordinate, start_time: int) -> dict:
        pass
    
    #Two stops_id + start time -> full informations about the route
    def get_full_route_stop(self, start_stop: int, end_stop: int, start_time: int) -> dict:
        reach_times = self.tdr.get_travel_line(start_stop, start_time)
        raw_route = find_raw_route(reach_times, start_stop, end_stop)
        print(raw_route)
        route = enhance_route(raw_route, self.stop_data, self.trip_data)
        # print(route)
        
        for it in range(len(route['trips'])):
            print(route['stops'][it])
            print(route['trips'][it])
        print(route['stops'][-1])
        return route

    #Common start coordinate + time -> in what time stops from end_ids list can be reached
    def get_reach_times(self, start: Coordinate, end_ids: List[int], start_time: int) -> dict:
        pass
    
    #In what time stops from end_ids can be reached if starting point is one of the stops from start_ids at given time
    def get_reach_times_stop(self, start_ids: List[int], end_ids: List[int], start_times: List[int]) -> dict:
        pass