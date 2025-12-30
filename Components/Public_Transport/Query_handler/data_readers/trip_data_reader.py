from .byte_reader import read_int, read_next_int, read_next_string, move_cursor

def read_trip_data_header(file):
    header = {}
    header['num_trips'] = read_int(file, 0, 2)
    header['lane_name_length'] = read_next_int(file, 1)
    header['single_trip_record_length'] = header['lane_name_length'] + 2
    header['trip_header_length'] = 3
    return header
    
def read_trip_data(file, header_info, trip_id):
    if trip_id == 0:
        return {'id': 0, 'lane_name': 'WALK'}
    initial_offset = (trip_id - 1) * header_info['single_trip_record_length'] + header_info['trip_header_length']
    move_cursor(file, initial_offset)
    trip_data = {}

    trip_data['id'] = read_next_int(file, 2)
    if trip_data['id'] != trip_id:
        raise ValueError(f"Trip ID mismatch: expected {trip_id}, got {trip_data['id']}")
    trip_data['lane_name'] = read_next_string(file, header_info['lane_name_length'])
    return trip_data