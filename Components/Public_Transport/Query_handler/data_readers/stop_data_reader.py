from .byte_reader import read_int, read_next_int, read_next_string, move_cursor

def read_stop_data_header(file):
    header = {}
    header['num_stops'] = read_int(file, 0, 2)
    header['stop_name_length'] = read_next_int(file, 1)
    header['stop_lat_length'] = read_next_int(file, 1)
    header['stop_lon_length'] = read_next_int(file, 1)
    header['single_stop_record_length'] = header['stop_name_length'] + header['stop_lat_length'] + header['stop_lon_length'] + 2
    header['stop_header_length'] = 5
    return header
    
def read_stop_data(file, header_info, stop_id):
    initial_offset = (stop_id - 1) * header_info['single_stop_record_length'] + header_info['stop_header_length']
    move_cursor(file, initial_offset)
    stop_data = {}
    stop_data['id'] = read_next_int(file, 2)
    if stop_data['id'] != stop_id:
        raise ValueError(f"Stop ID mismatch: expected {stop_id}, got {stop_data['id']}")
    stop_data['name'] = read_next_string(file, header_info['stop_name_length'])
    stop_data['lat'] = read_next_string(file, header_info['stop_lat_length'])
    stop_data['lon'] = read_next_string(file, header_info['stop_lon_length'])
    return stop_data