from Components.Map_Service.mapors_getters import matrix_durations

from typing import Tuple, List
Coordinate = Tuple[float, float] # (lat, lng)

def get_stop_coord(MPS, id):
    return (MPS.stop_data['stops'][id]['lat'], MPS.stop_data['stops'][id]['lng'])

class allStopsStrategy:
    def __init__(self, MPSClient):
        self.MPS = MPSClient
        pass

    def find_meeting_point(self, car_start_coord: Coordinate, pt_start_coord: Coordinate, finish_coord: Coordinate, 
                            car_start_time: int, pt_start_time: int):
        stop_ids = [i for i in range(1, self.MPS.stop_data['number_of_stops'] + 1)]
        pt_stop_reach_times = self.MPS.pt_client.get_reach_times(pt_start_coord, stop_ids, pt_start_time)

        mp_coords = [pt_start_coord, car_start_coord] + [get_stop_coord(self.MPS, stop_id) for stop_id in stop_ids]
        pt_mp_reach_times = [0, self.MPS.pt_client.get_reach_time(pt_start_coord, car_start_coord, pt_start_time)[0]] + [pt_stop_reach_time[0] for pt_stop_reach_time in pt_stop_reach_times]

        car_mp_durations = matrix_durations(self.MPS.ors_drive_client.matrix_s2d([car_start_coord], mp_coords))[0]
        car_mp_to_finish_durations = matrix_durations(self.MPS.ors_drive_client.matrix_s2d(mp_coords, [finish_coord]))

        car_mp_reach_times = [car_start_time + round(single_duration / 60) for single_duration in car_mp_durations]
        mp_reach_times = [max(car_reach_time, pt_reach_time) for car_reach_time, pt_reach_time in zip(car_mp_reach_times, pt_mp_reach_times)]

        best_reach_time = 1e9
        best_mp_reach_time = 1e9
        best_mp_id = -1
        for i in range(len(mp_reach_times)):
            reach_time = mp_reach_times[i] + round(car_mp_to_finish_durations[i][0] / 60)
            if best_reach_time > reach_time:
                best_reach_time = reach_time
                best_mp_id = i
                best_mp_reach_time = mp_reach_times[i]
            elif best_reach_time == reach_time and best_mp_reach_time > mp_reach_times[i]:
                best_reach_time = reach_time
                best_mp_id = i
                best_mp_reach_time = mp_reach_times[i]
        # coords of mp, eta, mp eta, car mp eta, pt mp eta
        return [mp_coords[best_mp_id], best_reach_time, best_mp_reach_time, car_mp_reach_times[best_mp_id], pt_mp_reach_times[best_mp_id]]