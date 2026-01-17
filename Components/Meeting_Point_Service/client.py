from Components.Map_Service.mapors_getters import single_duration
from Components.Meeting_Point_Service.strategy_all_stops import allStopsStrategy
from typing import Tuple

Coordinate = Tuple[float, float] # (lat, lng)

# TODO reverse order of returned coordinates 

class MPSClient:
    def __init__(self, ors_walk_client, ors_drive_client, map_client, pt_client):
        self.ors_walk_client = ors_walk_client
        self.ors_drive_client = ors_drive_client
        self.map_client = map_client
        self.pt_client = pt_client
        self.stop_data = pt_client.stop_data
        self.strategy = allStopsStrategy(self)
    
    def check_meeting_point(self, meeting_point_coord: Coordinate, car_start_coord: Coordinate, pt_start_coord: Coordinate, 
                            finish_coord: Coordinate, car_start_time: int, pt_start_time: int):
        pt_mp_reach_time = self.pt_client.get_reach_time(pt_start_coord, meeting_point_coord, pt_start_time)
        car_mp_reach_time = car_start_time + round(single_duration(
            self.ors_walk_client.simple_path([car_start_coord, meeting_point_coord])
            ) / 60)
        final_finish_reach_time = max(pt_mp_reach_time, car_mp_reach_time) + + round(single_duration(
            self.ors_drive_client.simple_path([meeting_point_coord, finish_coord])
            ) / 60)
        return final_finish_reach_time

    def get_meeting_point(self, car_start_coord: Coordinate, pt_start_coord: Coordinate, finish_coord: Coordinate, 
                           car_start_time: int, pt_start_time: int):
        pt_finish_reach_time = self.pt_client.get_reach_time(pt_start_coord, finish_coord, pt_start_time)[0]
        car_finish_reach_time = car_start_time + round(single_duration(
            self.ors_drive_client.simple_path([car_start_coord, finish_coord])
            ) / 60)
        if(pt_finish_reach_time <= car_finish_reach_time):
            # pt reach finish faster. No meeting point needed
            return [finish_coord, car_finish_reach_time, car_finish_reach_time, car_finish_reach_time, pt_finish_reach_time, 0]
        result = self.strategy.find_meeting_point(car_start_coord, pt_start_coord, finish_coord, car_start_time, pt_start_time)
        if result[1] >= pt_finish_reach_time:
            # no meeting point is better than direct routes
            return [finish_coord, pt_finish_reach_time, pt_finish_reach_time, car_finish_reach_time, pt_finish_reach_time, 0]
        return result + [1]

        