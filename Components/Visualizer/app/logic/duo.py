import time
import json
from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, current_app
from Components.Map_Service.mapors_getters import single_geometry, single_duration
from Components.Visualizer.app.logic.map_orders import MapOrders
from Components.Visualizer.app.logic.timeline_orders import TimelineOrders
from Components.Visualizer.app.logic.input_validator import get_point_from_geo_responce

car_color = "#3b82f6"
pt_color = "#8b5cf6" 
duo_color = "#10b981"

def time_to_str(time):
    time = time % (24 * 60)
    hours = time // 60
    minutes = time % 60
    return f"{hours:02d}:{minutes:02d}"

def pt_as_mp_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders):
    print("pt_meeting_point scenario", car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point)
    
    driver_path1 = current_app.ors_client_drive.simple_path([
        [car_start_address['lat'], car_start_address['lng']],
        [pt_start_address['lat'], pt_start_address['lng']]
        ])
    
    driver_path2 = current_app.ors_client_drive.simple_path([
        [pt_start_address['lat'], pt_start_address['lng']],
        [finish_address['lat'], finish_address['lng']]
    ])
    
    car_to_mp_time = carStartTime + round(single_duration(driver_path1) / 60)
    # pt_to_mp_time = pt_route_info['segments'][-1]['route'][-1]['arrival_time']
    mp_time = max(car_to_mp_time, ptStartTime)
    mp_to_finish_time = mp_time + round(single_duration(driver_path2) / 60)

    timeline_orders.set_main_header(meeting_point['name'], min(carStartTime, ptStartTime), mp_to_finish_time)
    timeline_orders.set_little_header("car", carStartTime, car_to_mp_time)
    # timeline_orders.set_little_header("pt", ptStartTime, pt_to_mp_time)
    timeline_orders.set_little_header("duo", mp_time, mp_to_finish_time)

    timeline_orders.add_car("car", driver_path1, car_start_address['name'], pt_start_address['name'], carStartTime, car_color)
    timeline_orders.add_car("duo", driver_path2, pt_start_address['name'], finish_address['name'], mp_time, duo_color)

    map_orders.add_car(driver_path1, f"Car route to meeting point <br> ETA: {time_to_str(car_to_mp_time)}", car_color)
    map_orders.add_car(driver_path2, f"Car route to destination <br> ETA: {time_to_str(mp_to_finish_time)}", duo_color)

def car_as_mp_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders):
    driver_path = current_app.ors_client_drive.simple_path([
        [car_start_address['lat'], car_start_address['lng']],
        [finish_address['lat'], finish_address['lng']]
        ])

    pt_route_info = current_app.pt_client.get_full_route(
        (pt_start_address['lat'], pt_start_address['lng']),
        (car_start_address['lat'], car_start_address['lng']),
        ptStartTime,
        pt_start_address['name'],
        car_start_address['name']
        )
    
    pt_to_mp_time = pt_route_info['segments'][-1]['route'][-1]['arrival_time']
    mp_time = max(carStartTime, pt_to_mp_time)
    car_to_finish_time = mp_time + round(single_duration(driver_path) / 60)
    # mp_time = max(car_to_mp_time, pt_to_mp_time)
    # mp_to_finish_time = mp_time + round(single_duration(driver_path2) / 60)

    timeline_orders.set_main_header(meeting_point['name'], min(carStartTime, ptStartTime), car_to_finish_time)
    # timeline_orders.set_little_header("car", carStartTime, car_to_finish_time)
    timeline_orders.set_little_header("pt", ptStartTime, pt_to_mp_time)
    timeline_orders.set_little_header("duo", mp_time, car_to_finish_time)

    # timeline_orders.add_car("car", driver_path, car_start_address['name'], finish_address['name'], carStartTime, car_color)
    timeline_orders.add_car("duo", driver_path, car_start_address['name'], finish_address['name'], mp_time, duo_color)

    # map_orders.add_car(driver_path, f"Car route to destination <br> ETA: {time_to_str(car_to_finish_time)}", car_color)
    map_orders.add_car(driver_path, f"Car route to destination <br> ETA: {time_to_str(car_to_finish_time)}", duo_color)

    for segment in pt_route_info['segments']:
        segment_coords = []
        for stop in segment['route']:
            segment_coords.append((stop['lat'], stop['lng']))
            stop['name'] = stop['name'].strip('"')
            # segment['route'][0]['name'] = segment['route'][0]['name'].strip('"')
            # segment['route'][-1]['name'] = segment['route'][-1]['name'].strip('"')
        if segment['type'] == 'walk':
            pt_path = current_app.ors_client_walk.simple_path(segment_coords)
            map_orders.add_walk(pt_path, f"Walk to: {segment['route'][-1]['name']}", pt_color)
            timeline_orders.add_pt_walk("pt", segment, pt_path)
        else:
            pt_path = current_app.ors_client_drive.simple_path(segment_coords)
            map_orders.add_car(pt_path, f"Take line {segment['line_name']} to: {segment['route'][-1]['name']}", pt_color)
            timeline_orders.add_pt("pt", segment)

def finish_as_mp_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders):
    driver_path = current_app.ors_client_drive.simple_path([
        [car_start_address['lat'], car_start_address['lng']],
        [finish_address['lat'], finish_address['lng']]
        ])

    pt_route_info = current_app.pt_client.get_full_route(
        (pt_start_address['lat'], pt_start_address['lng']),
        (finish_address['lat'], finish_address['lng']),
        ptStartTime,
        pt_start_address['name'],
        finish_address['name']
        )
    
    car_to_finish_time = carStartTime + round(single_duration(driver_path) / 60)
    pt_to_finish_time = pt_route_info['segments'][-1]['route'][-1]['arrival_time']
    # mp_time = max(car_to_mp_time, pt_to_mp_time)
    # mp_to_finish_time = mp_time + round(single_duration(driver_path2) / 60)

    timeline_orders.set_main_header(meeting_point['name'], min(carStartTime, ptStartTime), max(car_to_finish_time, pt_to_finish_time))
    timeline_orders.set_little_header("car", carStartTime, car_to_finish_time)
    timeline_orders.set_little_header("pt", ptStartTime, pt_to_finish_time)
    # timeline_orders.set_little_header("duo", mp_time, mp_to_finish_time)

    timeline_orders.add_car("car", driver_path, car_start_address['name'], finish_address['name'], carStartTime, car_color)
    # timeline_orders.add_car("duo", driver_path2, meeting_point['name'], finish_address['name'], mp_time, duo_color)

    map_orders.add_car(driver_path, f"Car route to destination <br> ETA: {time_to_str(car_to_finish_time)}", car_color)
    # map_orders.add_car(driver_path2, f"Car route to destination <br> ETA: {time_to_str(mp_to_finish_time)}", duo_color)

    for segment in pt_route_info['segments']:
        segment_coords = []
        for stop in segment['route']:
            segment_coords.append((stop['lat'], stop['lng']))
            stop['name'] = stop['name'].strip('"')
            # segment['route'][0]['name'] = segment['route'][0]['name'].strip('"')
            # segment['route'][-1]['name'] = segment['route'][-1]['name'].strip('"')
        if segment['type'] == 'walk':
            pt_path = current_app.ors_client_walk.simple_path(segment_coords)
            map_orders.add_walk(pt_path, f"Walk to: {segment['route'][-1]['name']}", pt_color)
            timeline_orders.add_pt_walk("pt", segment, pt_path)
        else:
            pt_path = current_app.ors_client_drive.simple_path(segment_coords)
            map_orders.add_car(pt_path, f"Take line {segment['line_name']} to: {segment['route'][-1]['name']}", pt_color)
            timeline_orders.add_pt("pt", segment)
    
    # map_orders.main_marker_update((meeting_point['lat'], meeting_point['lng']), 
    #                               meeting_point['name'] + "<br>ETA: " + time_to_str(mp_time), 
    #                               "meetingMarker")

def normal_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders):
    driver_path1 = current_app.ors_client_drive.simple_path([
        [car_start_address['lat'], car_start_address['lng']],
        [meeting_point['lat'], meeting_point['lng']]
        ])
    
    driver_path2 = current_app.ors_client_drive.simple_path([
        [meeting_point['lat'], meeting_point['lng']],
        [finish_address['lat'], finish_address['lng']]
    ])

    pt_route_info = current_app.pt_client.get_full_route(
        (pt_start_address['lat'], pt_start_address['lng']),
        (meeting_point['lat'], meeting_point['lng']),
        ptStartTime,
        pt_start_address['name'],
        meeting_point['name']
        )
    
    car_to_mp_time = carStartTime + round(single_duration(driver_path1) / 60)
    pt_to_mp_time = pt_route_info['segments'][-1]['route'][-1]['arrival_time']
    mp_time = max(car_to_mp_time, pt_to_mp_time)
    mp_to_finish_time = mp_time + round(single_duration(driver_path2) / 60)

    timeline_orders.set_main_header(meeting_point['name'], min(carStartTime, ptStartTime), mp_to_finish_time)
    timeline_orders.set_little_header("car", carStartTime, car_to_mp_time)
    timeline_orders.set_little_header("pt", ptStartTime, pt_to_mp_time)
    timeline_orders.set_little_header("duo", mp_time, mp_to_finish_time)

    timeline_orders.add_car("car", driver_path1, car_start_address['name'], meeting_point['name'], carStartTime, car_color)
    timeline_orders.add_car("duo", driver_path2, meeting_point['name'], finish_address['name'], mp_time, duo_color)

    map_orders.add_car(driver_path1, f"Car route to meeting point <br> ETA: {time_to_str(car_to_mp_time)}", car_color)
    map_orders.add_car(driver_path2, f"Car route to destination <br> ETA: {time_to_str(mp_to_finish_time)}", duo_color)

    for segment in pt_route_info['segments']:
        segment_coords = []
        for stop in segment['route']:
            segment_coords.append((stop['lat'], stop['lng']))
            stop['name'] = stop['name'].strip('"')
            # segment['route'][0]['name'] = segment['route'][0]['name'].strip('"')
            # segment['route'][-1]['name'] = segment['route'][-1]['name'].strip('"')
        if segment['type'] == 'walk':
            pt_path = current_app.ors_client_walk.simple_path(segment_coords)
            map_orders.add_walk(pt_path, f"Walk to: {segment['route'][-1]['name']}", pt_color)
            timeline_orders.add_pt_walk("pt", segment, pt_path)
        else:
            pt_path = current_app.ors_client_drive.simple_path(segment_coords)
            map_orders.add_car(pt_path, f"Take line {segment['line_name']} to: {segment['route'][-1]['name']}", pt_color)
            timeline_orders.add_pt("pt", segment)
    
    map_orders.main_marker_update((meeting_point['lat'], meeting_point['lng']), 
                                  meeting_point['name'] + "<br>ETA: " + time_to_str(mp_time), 
                                  "meetingMarker")


duo_bp = Blueprint('duo_bp', __name__)

@duo_bp.route('/')
def show_site():
    return render_template('main_view.html')

@duo_bp.route('/duo/computing', methods=["POST"])
def compute_routes():
    logfile = open("log.txt", "w")
    counter_start_time = time.perf_counter()
    
    current_time = datetime.now().minute + datetime.now().hour * 60
    input_form = request.get_json()
    
    print("Compute Duo input: ", file=logfile)
    print(json.dumps(input_form), file=logfile)

    car_start_address = input_form['addresses']['carStartAddress']
    pt_start_address = input_form['addresses']['ptStartAddress']
    finish_address = input_form['addresses']['finishAddress']
    if not finish_address['valid'] or not car_start_address['valid'] or not pt_start_address['valid']:
        return jsonify(valid=False, message="Invalid query")

    if input_form['times']['carStartTime']['valid']:
        carStartTime = input_form['times']['carStartTime']['hour'] * 60 + input_form['times']['carStartTime']['minute']
    else:
        carStartTime = current_time

    if input_form['times']['ptStartTime']['valid']:
        ptStartTime = input_form['times']['ptStartTime']['hour'] * 60 + input_form['times']['ptStartTime']['minute']
    else:
        ptStartTime = current_time

    strategy_variant = input_form['strategy']
    print("Strategy variant:", strategy_variant)

    # if not car_start_address['valid'] or not pt_start_address['valid'] or not finish_address:
    #     return jsonify(valid=False, message="Invalid addresses")
    
    # coords of mp, eta, mp eta, car mp eta, pt mp eta
    # coords of mp, variant, mp name
    mp_coords, variant, mp_name = current_app.mps_client.get_meeting_point(
        (car_start_address['lat'], car_start_address['lng']),
        (pt_start_address['lat'], pt_start_address['lng']),
        (finish_address['lat'], finish_address['lng']),
        carStartTime,
        ptStartTime,
        strategy_variant
    )
    mp_name = mp_name.strip('"') if mp_name is not None else None
    # mp_coords, variant, mp_name = meeting_point_raw_data

    print("Found meeting point: ", mp_coords, variant, mp_name)
    print("thinked for: ", time.perf_counter() - counter_start_time)

    meeting_point = {}
    meeting_point['lat'] = float(mp_coords[0])
    meeting_point['lng'] = float(mp_coords[1])

    if mp_name is not None:
        meeting_point['name'] = mp_name
    elif variant == 1:
        meeting_point['name'] = "Driver start location"
    elif variant == 2:
        meeting_point['name'] = "Passenger start location"
    elif variant == 3:
        meeting_point['name'] = "Destination"
    else:
        point = get_point_from_geo_responce(
            current_app.geo_client.reverse_geocode([meeting_point['lat'], meeting_point['lng']])
        )
        print("Reverse geocoded point:", point)
        meeting_point['name'] = point['name']
    
    print("Final meeting point", meeting_point)

    map_orders = MapOrders()
    timeline_orders = TimelineOrders()

    if variant == 0:
        normal_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders)
    elif variant == 1:
        car_as_mp_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders)
    elif variant == 2:
        pt_as_mp_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders)
    elif variant == 3:
        finish_as_mp_scenario(car_start_address, pt_start_address, finish_address, carStartTime, ptStartTime, meeting_point, input_form, map_orders, timeline_orders)
    
    print("All took: ", time.perf_counter() - counter_start_time)
    orders = {
        "map": map_orders.get_orders(),
        "timeline" : timeline_orders.get_orders()
    }
    print("Pass orders to frontend")
    print(json.dumps(orders), file=logfile)
    logfile.close()
    return orders
    