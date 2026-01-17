from Components.Public_Transport.Client.data_readers.byte_reader import read_int, read_next_int, move_cursor

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
        schedule_record = [[0, 0, 0]]
        move_cursor(self.file, initial_offset)
        for stop_id in range(1, num_stops + 1):
            single_record = []
            single_record.append(read_next_int(self.file, 2))  # arrival_time
            single_record.append(read_next_int(self.file, 2))  # previous stop
            single_record.append(read_next_int(self.file, 2))  # last trip id
            schedule_record.append(single_record)
        return schedule_record

    def read_single_travel_batch(self, start_stop, start_time, end_stop):
        num_stops = self.header['num_stops']
        initial_offset = (((start_stop - 1) * self.minutes_in_day  + start_time) * num_stops + end_stop - 1) * self.single_record_size + self.header['schedule_header_length']
        data_batch = []
        move_cursor(self.file, initial_offset)
        data_batch.append(read_next_int(self.file, 2))  # arrival_time
        data_batch.append(read_next_int(self.file, 2))  # previous stop
        data_batch.append(read_next_int(self.file, 2))  # last trip id
        return data_batch