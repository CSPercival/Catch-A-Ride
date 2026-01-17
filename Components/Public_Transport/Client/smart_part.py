def find_crucial_stops(arrival_data, start_stop, dest_stop):
    route = []
    current_stop = dest_stop
    while(current_stop != start_stop):
        route.append([current_stop, arrival_data[current_stop][0], arrival_data[current_stop][2]]) # stop_id, arrival_time, trip_id
        current_stop = arrival_data[current_stop][1]
    route.append([start_stop, arrival_data[start_stop][0], 0])
    route.reverse()
    return route

def find_raw_route(raw_route, stop_data, trip_data):
    route = {}
    stops = [stop_data['stops'][raw_route[0][0]].copy()]
    stops[0]['arrival_time'] = raw_route[0][1]
    trips = []
    for stop in raw_route[1:]:
        stops.append(stop_data['stops'][stop[0]].copy())
        stops[-1]['arrival_time'] = stop[1]
        trips.append(trip_data['trips'][stop[2]].copy())
    route['stops'] = stops
    route['trips'] = trips
    return route

# segment = {
#     "type": "bus"|"tram"|"walk",
#     "line_name" : string,
#     "duration": int,
#     "route" : [
#         {
#             "id" : int,
#             "lat" : string,
#             "lng" : string,
#             "name" : string,
#             "old_id" : string,
#             "arrival_time" : int
#         },
#     ]
# }

def add_walk(route, stopA, stopB, start_time):
    route_segment = {}
    route_segment['type'] = "walk"
    route_segment['line_name'] = "walk"
    route_segment['duration'] = stopB['arrival_time'] - stopA['arrival_time']
    route_segment['route'] = [stopA.copy(), stopB.copy()]
    route_segment['route'][0]['arrival_time'] += start_time
    route_segment['route'][1]['arrival_time'] += start_time
    route['segments'].append(route_segment)


def add_pt_trip(route, stopA, stopB, trip, start_time, stop_data):
    route_segment = {}
    if(trip['line_name'].isdigit() and int(trip['line_name']) in range(100)):
        route_segment['type'] = "tram"
    else:
        route_segment['type'] = "bus"
    route_segment['line_name'] = trip['line_name']
    route_segment['route'] = []
    trip_active = False
    for v in trip['route']:
        if v['stop'] == stopA['id']:
            trip_active = True
        if not trip_active:
            continue
        route_segment['route'].append(stop_data['stops'][v['stop']].copy())
        route_segment['route'][-1]['arrival_time'] = v['time']
        if v['stop'] == stopB['id']:
            break
    route_segment['duration'] = route_segment['route'][-1]['arrival_time'] - route_segment['route'][0]['arrival_time']
    route['segments'].append(route_segment)


def enhance_route(route, stop_data, trip_data, start_time):
    new_route = {}
    new_route['duration'] = route['stops'][-1]['arrival_time'] - route['stops'][0]['arrival_time']
    new_route['segments'] = []
    last_stop = route['stops'][0]
    for i in range(len(route['trips'])):
        stop = route['stops'][i + 1]
        trip = route['trips'][i]
        if trip['id'] == 0:
            if i + 1 < len(route['trips']) and route['trips'][i + 1]['id'] == 0:
                continue
            add_walk(new_route, last_stop, stop, start_time)
        else :
            add_pt_trip(new_route, last_stop, stop, trip, start_time, stop_data)
        last_stop = stop
    return new_route
