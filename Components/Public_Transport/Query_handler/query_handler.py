from data_readers.schedule_data_reader import read_schedule_data_header, read_schedule_line, read_single_schedule_batch
from smart_part import find_route, decode_route

def get_route(start_stop, destination_stop, start_time, days_id):
    header_info = {}
    days_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    stop_path = "./../Resources/Preprocessed_Data/Common/Stop_Data.bin"
    trip_path = "./../Resources/Preprocessed_Data/" + days_names[days_id] + "/Trip_Data.bin"
    schedule_path = "./../Resources/Preprocessed_Data/" + days_names[days_id] + "/Schedule_Data.bin"

    schedule_data = []
    with open(schedule_path, 'rb') as schedule_file:
        header_info.update(read_schedule_data_header(schedule_file))
        schedule_data = read_schedule_line(schedule_file, start_stop, start_time, header_info)
    raw_route = find_route(schedule_data, start_stop, destination_stop)

    with open(stop_path, 'rb') as stop_file, open(trip_path, 'rb') as trip_file:
        route = decode_route(raw_route, stop_file, trip_file)
    for it in range(len(route['trips'])):
        print(route['stops'][it])
        print(route['trips'][it])
    print(route['stops'][-1])
    return route



def get_arrival_time(start_stop, destination_stop, start_time, days_id):
    header_info = {}
    days_names = {0: "Mon-Thu", 1: "Fri", 2: "Sat", 3: "Sun"}
    schedule_path = "./../Resources/Preprocessed_Data/" + days_names[days_id] + "/Schedule_Data.bin"

    destionation_batch = []
    with open(schedule_path, 'rb') as schedule_file:
        header_info.update(read_schedule_data_header(schedule_file))
        destionation_batch = read_single_schedule_batch(schedule_file, start_stop, start_time, destination_stop, header_info)
    return destionation_batch[0]


# if __name__ == "__main__":
#     # get_route(1749, 2324, 480, 0)
#     get_route(2, 10, 480, 0)