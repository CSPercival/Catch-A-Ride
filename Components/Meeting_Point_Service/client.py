from Components.Map_Service.mapors_getters import single_duration
from Components.Meeting_Point_Service.strategy_all_stops import allStopsStrategy
from Components.Meeting_Point_Service.strategy_isochrones import isochronesStrategy
from typing import Tuple

Coordinate = Tuple[float, float] # (lat, lng)

# TODO reverse order of returned coordinates 

class MPSClient:
    def __init__(self, ors_walk_client, ors_drive_client, geo_client, pt_client):
        self.ors_walk_client = ors_walk_client
        self.ors_drive_client = ors_drive_client
        self.geo_client = geo_client
        self.pt_client = pt_client
        self.stop_data = pt_client.stop_data
        self.strategies = []
        self.strategies.append(allStopsStrategy(self))
        self.strategies.append(isochronesStrategy(self))

    
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

    # coords of mp, eta, mp eta, car mp eta, pt mp eta
    # TODO check if (forgot)
    # 0 - new meeting point, 1 - car_start_coord, 2 - pt_start_coord, 3 - finish_coord
    def get_meeting_point(self, car_start_coord: Coordinate, pt_start_coord: Coordinate, finish_coord: Coordinate, 
                           car_start_time: int, pt_start_time: int, strategy_variant: int):
        pt_finish_reach_time = self.pt_client.get_reach_time(pt_start_coord, finish_coord, pt_start_time)[0]
        car_finish_reach_time = car_start_time + round(single_duration(
            self.ors_drive_client.simple_path([car_start_coord, finish_coord])
            ) / 60)
        if pt_finish_reach_time <= car_finish_reach_time:
            # pt reach finish faster. No meeting point needed
            return [finish_coord, 3, None]
            # return [
            #         finish_coord, # mp coord
            #         car_finish_reach_time, # eta
            #         car_finish_reach_time, # mp eta
            #         car_finish_reach_time, # car mp eta
            #         pt_finish_reach_time, # pt mp eta
            #         0
            #         ]
        
        car_pt_reach_time = None
        if car_start_time < pt_start_time:
            car_pt_reach_time = car_start_time + round(single_duration(
                self.ors_drive_client.simple_path([car_start_coord, pt_start_coord])
                ) / 60)
            if car_pt_reach_time <= pt_start_time:
                # car can reach pt start before pt starts. No meeting point needed
                # car_pt_finish_reach_time = pt_start_time + round(single_duration(
                #     self.ors_drive_client.simple_path([pt_start_coord, finish_coord])
                #     ) / 60)
                return [pt_start_coord, 2, None]
                # return [
                #     pt_start_coord, # mp coord
                #     car_pt_finish_reach_time, # eta
                #     pt_start_time, # mp eta
                #     car_pt_reach_time, # car mp eta
                #     pt_start_time, # pt mp eta
                #     0
                #     ]
        
        mp_coords, reach_time, variant, mp_name = (
            self.strategies[strategy_variant].find_meeting_point(
                car_start_coord, 
                pt_start_coord, 
                finish_coord, 
                car_start_time, 
                pt_start_time, 
                [car_finish_reach_time, pt_finish_reach_time, car_pt_reach_time]))
        if strategy_variant == 1 and variant == 3:
            mp_coords, reach_time, variant, mp_name = (
                self.strategies[0].find_meeting_point(
                    car_start_coord, 
                    pt_start_coord, 
                    finish_coord, 
                    car_start_time, 
                    pt_start_time, 
                    [car_finish_reach_time, pt_finish_reach_time, car_pt_reach_time]))

        if reach_time >= pt_finish_reach_time:
            # no meeting point is better than direct routes
            # return [finish_coord, pt_finish_reach_time, pt_finish_reach_time, car_finish_reach_time, pt_finish_reach_time, 0]
            return [finish_coord, 3, None]
        return [mp_coords, variant, mp_name]

    def test_strategy(self, car_start_coord: Coordinate, pt_start_coord: Coordinate, finish_coord: Coordinate, 
                           car_start_time: int, pt_start_time: int):
        return self.strategy.find_meeting_point(car_start_coord, pt_start_coord, finish_coord, car_start_time, pt_start_time, [0])
        