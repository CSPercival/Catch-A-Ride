from .byte_reader import read_int, read_next_int, move_cursor

def read_schedule_data_header(file):
    header = {}
    header['num_stops'] = read_int(file, 0, 2)
    header['schedule_header_length'] = 2
    return header
    
def read_schedule_line(file, start_stop, start_time, header_info):
    minutes_in_day = 24 * 60
    num_stops = header_info['num_stops']
    single_record_size = 6
    initial_offset = ((start_stop - 1) * minutes_in_day  + start_time) * single_record_size * (num_stops - 1) + header_info['schedule_header_length']
    schedule_record = [[0, 0, 0]]
    move_cursor(file, initial_offset)
    for stop_id in range(1, num_stops):
        single_record = []
        single_record.append(read_next_int(file, 2))  # arrival_time
        single_record.append(read_next_int(file, 2))  # previous stop
        single_record.append(read_next_int(file, 2))  # last trip id
        schedule_record.append(single_record)
    return schedule_record

def read_single_schedule_batch(file, start_stop, start_time, destination_stop, header_info):
    minutes_in_day = 24 * 60
    num_stops = header_info['num_stops']
    single_record_size = 6
    initial_offset = (((start_stop - 1) * minutes_in_day  + start_time) * num_stops + destination_stop - 1) * single_record_size + header_info['schedule_header_length']
    data_batch = []
    move_cursor(file, initial_offset)
    data_batch.append(read_next_int(file, 2))  # arrival_time
    data_batch.append(read_next_int(file, 2))  # previous stop
    data_batch.append(read_next_int(file, 2))  # last trip id
    return data_batch