from Components.Map_Service.mapors_getters import single_segment_durations

from typing import Tuple, List
Coordinate = Tuple[float, float] # (lat, lng)

def get_stop_coord(MPS, id):
    return (MPS.stop_data['stops'][id]['lat'], MPS.stop_data['stops'][id]['lng'])

def round_to_min(times):
    return [round(time / 60) for time in times]

class isochronesStrategy:
    def __init__(self, MPSClient):
        self.MPS = MPSClient
        pass

    def find_meeting_point(self, car_start_coord: Coordinate, pt_start_coord: Coordinate, finish_coord: Coordinate, 
                            car_start_time: int, pt_start_time: int, additional_info: List[int]):
        # tmp_times = round_to_min(
        #     single_segment_durations(
        #         self.MPS.ors_drive_client.simple_path([car_start_coord, pt_start_coord, finish_coord])
        #     )
        # )
        # car_to_pt_car = tmp_times[0]
        # car_to_finish_car = additional_info[0]
        # pt_to_finish_car = tmp_times[1]
        # pt_to_finish_pt = additional_info[1]
        
        # stop_ids = [i for i in range(1, self.MPS.stop_data['number_of_stops'] + 1)]
        # # pt_stop_reach_times = self.MPS.pt_client.get_reach_times(pt_start_coord, stop_ids, pt_start_time)
        # pt_stop_times = [pt_start_time] + [pt_stop_time[0] for pt_stop_time 
        #                                          in self.MPS.pt_client.get_reach_times(pt_start_coord, stop_ids, pt_start_time)]

        # car_isochrones = self.MPS.ors_drive_client.isochrones([car_start_coord], [min(3600, 60 * (car_to_pt_car + pt_to_finish_car))], interval=60)
        # finish_isochrones = self.MPS.ors_drive_client.isochrones([finish_coord], [min(3600, 60 * (pt_to_finish_car + 10))], interval=60)

        # lower_time_limit = max(pt_start_time, car_start_time)
        # upper_time_limit = min(car_start_time + car_to_pt_car + pt_to_finish_car, 
        #                        pt_to_finish_pt)
        
        # for time_for_meeting in range(lower_time_limit, upper_time_limit + 1):


        # return car_times
        # tmp_result = self.MPS.ors_drive_client.simple_path([car_start_coord, pt_start_coord, finish_coord])
        # return tmp_result
        
        result = self.MPS.ors_walk_client.isochrones([pt_start_coord], [3600], interval=60)
        return result
    # def isochrones(self, coordinates: Coordinate, range: List[int], range_type: str = None, intersections: bool = False) -> dict:

        # stop_ids = [i for i in range(1, self.MPS.stop_data['number_of_stops'] + 1)]
        # pt_stop_reach_times = self.MPS.pt_client.get_reach_times(pt_start_coord, stop_ids, pt_start_time)

        # mp_coords = [pt_start_coord, car_start_coord] + [get_stop_coord(self.MPS, stop_id) for stop_id in stop_ids]
        # pt_mp_reach_times = [0, self.MPS.pt_client.get_reach_time(pt_start_coord, car_start_coord, pt_start_time)[0]] + [pt_stop_reach_time[0] for pt_stop_reach_time in pt_stop_reach_times]

        # car_mp_durations = matrix_durations(self.MPS.ors_drive_client.matrix_s2d([car_start_coord], mp_coords))[0]
        # car_mp_to_finish_durations = matrix_durations(self.MPS.ors_drive_client.matrix_s2d(mp_coords, [finish_coord]))

        # car_mp_reach_times = [car_start_time + round(single_duration / 60) for single_duration in car_mp_durations]
        # mp_reach_times = [max(car_reach_time, pt_reach_time) for car_reach_time, pt_reach_time in zip(car_mp_reach_times, pt_mp_reach_times)]

        # best_reach_time = 1e9
        # # best_mp_reach_time = 1e9
        # lowest_pt_tt = 1e9
        # best_mp_id = -1
        # for i in range(len(mp_reach_times)):
        #     reach_time = mp_reach_times[i] + round(car_mp_to_finish_durations[i][0] / 60)
        #     if best_reach_time > reach_time:
        #         best_reach_time = reach_time
        #         best_mp_id = i
        #         lowest_pt_tt = pt_mp_reach_times[i]
        #     elif best_reach_time == reach_time and lowest_pt_tt > pt_mp_reach_times[i]:
        #         best_reach_time = reach_time
        #         best_mp_id = i
        #         lowest_pt_tt = pt_mp_reach_times[i]
        # # coords of mp, eta, mp eta, car mp eta, pt mp eta
        # return [mp_coords[best_mp_id], best_reach_time, mp_reach_times[best_mp_id], car_mp_reach_times[best_mp_id], pt_mp_reach_times[best_mp_id]]