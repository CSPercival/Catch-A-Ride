from Components.Map_Service.mapors_getters import single_segment_durations
from shapely.geometry import Polygon, Point, LineString
from typing import Tuple, List
Coordinate = Tuple[float, float] # (lat, lng)

def get_stop_coord(MPS, id):
    return (MPS.stop_data['stops'][id]['lat'], MPS.stop_data['stops'][id]['lng'])

def round_to_min(times):
    return [round(time / 60) for time in times]

def reduce_to_convex_hull(shape):
    if shape.is_empty:
        return shape
    return shape.convex_hull

def to_shape(list_of_coords_in):
    coords = [(c[0], c[1]) for c in list_of_coords_in]
    if not coords:
        return Point(0, 0)
    if len(coords) == 1:
        geom = Point(coords[0])
    elif len(coords) == 2:
        geom = LineString(coords)
    else:
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        geom = Polygon(coords)

    return geom


class isochronesStrategy:
    def __init__(self, MPSClient):
        self.MPS = MPSClient
        pass

    def get_isochrone(self, isochrones, time):
        time = min(time, len(isochrones) - 1)
        return isochrones[time]

    def intersection_wrap(self, iso1, iso2):
        iso1_convex = reduce_to_convex_hull(iso1)
        iso2_convex = reduce_to_convex_hull(iso2)
        intersection = iso1_convex.intersection(iso2_convex)
        if intersection.is_empty:
            return intersection
        
        intersection = iso1.intersection(iso2)
        if not intersection.is_empty:
            return intersection
        intersection = iso2.intersection(iso1)
        if not intersection.is_empty:
            return intersection
        
        iso1 = reduce_to_convex_hull(iso1)
        intersection = iso1.intersection(iso2)
        if not intersection.is_empty:
            return intersection
        intersection = iso2.intersection(iso1)
        if not intersection.is_empty:
            return intersection
        
        iso2 = reduce_to_convex_hull(iso2)
        intersection = iso1.intersection(iso2)
        if not intersection.is_empty:
            return intersection
        intersection = iso2.intersection(iso1)
        return intersection

    def _get_finish_time(self, meeting_areas, finish_isochrones):
        max_shape = to_shape(self.get_isochrone(finish_isochrones, len(finish_isochrones)))
        meeting_areas = [meeting_area for meeting_area in meeting_areas 
                         if not self.intersection_wrap(meeting_area, max_shape).is_empty]
        
        print("     Meeting areas after filtering with finish isochrone: ", len(meeting_areas), flush=True)

        best_time = 1e9
        for meeting_area in meeting_areas:
            lower_time_limit = -1
            upper_time_limit = len(finish_isochrones) - 1
            while lower_time_limit + 1 < upper_time_limit:
                middle_time = (lower_time_limit + upper_time_limit) // 2
                if self.intersection_wrap(meeting_area, to_shape(self.get_isochrone(finish_isochrones, middle_time))).is_empty:
                    lower_time_limit = middle_time
                else:
                    upper_time_limit = middle_time
            best_time = min(best_time, upper_time_limit)
        return best_time

    def _get_meeting_areas(self, meeting_time, car_start_time, pt_start_time, car_isochrones, pt_walk_isochrones, stop_isochrones):
        meeting_areas = []
        
        car_polygon = to_shape(self.get_isochrone(car_isochrones, meeting_time - car_start_time))
        walk_polygon = to_shape(self.get_isochrone(pt_walk_isochrones, meeting_time - pt_start_time))
        meeting_area = self.intersection_wrap(walk_polygon, car_polygon)
        if not meeting_area.is_empty:
            meeting_areas.append(reduce_to_convex_hull(meeting_area))
        
        for stop_area in stop_isochrones:
            stop_polygon = to_shape(stop_area)
            meeting_area = self.intersection_wrap(stop_polygon, car_polygon)
            if not meeting_area.is_empty:
                meeting_areas.append(reduce_to_convex_hull(meeting_area))
        return meeting_areas
    
    def _get_meeting_point(self, time_to_finish, meeting_areas, finish_isochrones):
        finish_area = to_shape(self.get_isochrone(finish_isochrones, time_to_finish))
        for meeting_area in meeting_areas:
            # intersection = finish_area.intersection(meeting_area)
            intersection = self.intersection_wrap(meeting_area, finish_area)
            if not intersection.is_empty:
                return (intersection.representative_point().x, intersection.representative_point().y)
        raise ValueError("No meeting point found in the intersection of meeting areas and finish isochrone") 

    
    def find_meeting_point(self, car_start_coord: Coordinate, pt_start_coord: Coordinate, finish_coord: Coordinate, 
                            car_start_time: int, pt_start_time: int, additional_info: List[int]):
        tmp_times = round_to_min(
            single_segment_durations(
                self.MPS.ors_drive_client.simple_path([car_start_coord, pt_start_coord, finish_coord])
            )
        )
        car_to_pt_car = tmp_times[0]
        # car_to_finish_car = additional_info[0]
        pt_to_finish_car = tmp_times[1]
        pt_to_finish_pt = additional_info[1]
        
        stop_ids = [i for i in range(1, self.MPS.stop_data['number_of_stops'] + 1)]
        pt_stop_reach_times_raw = self.MPS.pt_client.get_reach_times(pt_start_coord, stop_ids, pt_start_time)
        pt_stop_reach_times =  [pt_stop_reach_time[0] for pt_stop_reach_time in pt_stop_reach_times_raw]

        upper_time_limit = min((car_start_time + car_to_pt_car + pt_to_finish_car), pt_to_finish_pt)
        lower_time_limit = max(car_start_time, pt_start_time)
        car_isochrones = self.MPS.ors_drive_client.range_isochrones_geometries(
            car_start_coord, min(3600, 60 * (upper_time_limit - car_start_time)), interval=60, smoothing=5)
        finish_isochrones = self.MPS.ors_drive_client.range_isochrones_geometries(
            finish_coord, min(3600, 60 * (upper_time_limit - lower_time_limit)), interval=60, smoothing=5)
        pt_walk_isochrones = self.MPS.ors_walk_client.range_isochrones_geometries(
            pt_start_coord, min(3600, 60 * (upper_time_limit - lower_time_limit)), interval=60, smoothing=5)
        
        print("Computation of isochrones finished", flush=True)

        best_overall_time = upper_time_limit
        best_meeting_time = None
        print("Checking meeting times from", lower_time_limit, "to", upper_time_limit, flush=True)
        for meeting_time in range(lower_time_limit, upper_time_limit + 1):
            print("Checking meeting time", meeting_time, flush=True)
            stop_isochrones = self.MPS.pt_client.isochrones(stop_ids, pt_stop_reach_times, meeting_time)
            print("     Stop isochrones: ", len(stop_isochrones), flush=True)
            meeting_areas = self._get_meeting_areas(meeting_time, car_start_time, pt_start_time, car_isochrones, pt_walk_isochrones, stop_isochrones)
            print("     Meeting areas: ", len(meeting_areas), flush=True)
            if len(meeting_areas) > 0:
                mp_to_finish_time = self._get_finish_time(meeting_areas, finish_isochrones)
                print("     Time to finish from meeting area: ", mp_to_finish_time, flush=True)
                if meeting_time + mp_to_finish_time < best_overall_time:
                    best_overall_time = meeting_time + mp_to_finish_time
                    best_meeting_time = meeting_time
        
        # mp_coords, reach_time, variant, mp_name
        print("Best overall time:", best_overall_time, flush=True)
        print("Best meeting time:", best_meeting_time, flush=True)
        if best_meeting_time is None or best_overall_time == upper_time_limit:
            # no meeting point is better than direct routes
            return [finish_coord, upper_time_limit, 3, None]

        stop_isochrones = self.MPS.pt_client.isochrones(stop_ids, pt_stop_reach_times, best_meeting_time)
        meeting_areas = self._get_meeting_areas(best_meeting_time, car_start_time, pt_start_time, car_isochrones, pt_walk_isochrones, stop_isochrones)
        meeting_point = self._get_meeting_point(best_overall_time - best_meeting_time, meeting_areas, finish_isochrones)
    # def _snap(self, coordinate: Coordinate, radius = 10) -> Coordinate:
        meeting_point = self.MPS.ors_drive_client._snap(meeting_point, 100)
        print("Meeting point found at:", meeting_point, flush=True)
        return [meeting_point, best_overall_time, 0, None]