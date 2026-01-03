from data_readers.stop_data_reader import read_stop_data_header, read_stop_data 
from data_readers.trip_data_reader import read_trip_data_header, read_trip_data

def find_route(arrival_data, start_stop, dest_stop):
    route = []
    current_stop = dest_stop
    while(current_stop != start_stop):
        route.append([current_stop, arrival_data[current_stop][0], arrival_data[current_stop][2]]) # stop_id, arrival_time, trip_id
        current_stop = arrival_data[current_stop][1]
    route.append([start_stop, arrival_data[start_stop][0], 0])
    route.reverse()
    return route

def decode_route(raw_route, stop_file, trip_file):
    header_info = {}
    header_info.update(read_stop_data_header(stop_file))
    header_info.update(read_trip_data_header(trip_file))
    route = {}
    stops = [read_stop_data(stop_file, header_info, raw_route[0][0])]
    stops[0]['arrival_time'] = raw_route[0][1]
    trips = []
    for stop in raw_route[1:]:
        stops.append(read_stop_data(stop_file, header_info, stop[0]))
        stops[-1]['arrival_time'] = stop[1]
        trips.append(read_trip_data(trip_file, header_info, stop[2]))
    route['stops'] = stops
    route['trips'] = trips
    return route