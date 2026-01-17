def get_single_stop_coords(id, stop_data):
    return (float(stop_data['stops'][id]['lat']), float(stop_data['stops'][id]['lng']))

def get_stops_coords(ids, stop_data):
        return [get_single_stop_coords(id, stop_data) for id in ids]