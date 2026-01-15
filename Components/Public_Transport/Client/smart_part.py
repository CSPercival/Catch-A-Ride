def find_raw_route(arrival_data, start_stop, dest_stop):
    route = []
    current_stop = dest_stop
    while(current_stop != start_stop):
        route.append([current_stop, arrival_data[current_stop][0], arrival_data[current_stop][2]]) # stop_id, arrival_time, trip_id
        current_stop = arrival_data[current_stop][1]
    route.append([start_stop, arrival_data[start_stop][0], 0])
    route.reverse()
    return route

def enhance_route(raw_route, stop_data, trip_data):
    route = {}
    stops = [stop_data['stops'][raw_route[0][0]]]
    stops[0]['arrival_time'] = raw_route[0][1]
    trips = []
    for stop in raw_route[1:]:
        stops.append(stop_data['stops'][stop[0]])
        stops[-1]['arrival_time'] = stop[1]
        trips.append(trip_data['trips'][stop[2]])
    route['stops'] = stops
    route['trips'] = trips
    return route
