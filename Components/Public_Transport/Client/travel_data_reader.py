import struct

def read_bytes(file, offset, length):
    file.seek(offset)
    return file.read(length)

def move_cursor(file, offset):
    file.seek(offset)

def read_next_bytes(file, length):
    return file.read(length)

def read_int(file, offset, length):
    raw_bytes = read_bytes(file, offset, length)
    if length == 1:
        return struct.unpack('<b', raw_bytes)[0]
    elif length == 2:
        return struct.unpack('<h', raw_bytes)[0]
    elif length == 4:
        return struct.unpack('<i', raw_bytes)[0]
    else:
        raise ValueError("Unsupported integer byte length")

class Travel_Data_Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, "rb")
        self.minutes_in_day = 24 * 60
        self.single_record_size = 6

        self.header = {
            "num_stops" : read_int(self.file, 0, 2),
            "travel_header_length" : 2
        }
        
    def get_travel_line(self, start_stop, start_time):
        num_stops = self.header['num_stops']
        initial_offset = ((start_stop - 1) * self.minutes_in_day  + start_time) * self.single_record_size * num_stops + self.header['travel_header_length']
        travel_record = [[0, 0, 0]]
        move_cursor(self.file, initial_offset)
        buffer = read_next_bytes(self.file, num_stops * self.single_record_size)
        for batch in struct.iter_unpack('<hhh', buffer):
            travel_record.append(list(batch))
        return travel_record

    def read_single_travel_batch(self, start_stop, start_time, end_stop):
        num_stops = self.header['num_stops']
        initial_offset = (((start_stop - 1) * self.minutes_in_day  + start_time) * num_stops + end_stop - 1) * self.single_record_size + self.header['travel_header_length']
        move_cursor(self.file, initial_offset)
        buffer = read_next_bytes(self.file, self.single_record_size)
        data_batch = list(struct.unpack('<hhh', buffer))
        return data_batch