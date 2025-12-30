from data_readers.schedule_data_reader import read_schedule_data_header, read_schedule_line, read_single_schedule_batch
from smart_part import find_route, decode_route

def get_route(start_stop, destination_stop, start_time, days_id):
    header_info = {}
    days_names = {0: "Mon-Thu", 1: "Fri", 2: "Sat", 3: "Sun"}
    stop_path = "./../Resources/Preprocessed_Data/Common/Stop_Data.bin"
    trip_path = "./../Resources/Preprocessed_Data/" + days_names[days_id] + "/Trip_Data.bin"
    schedule_path = "./../Resources/Preprocessed_Data/" + days_names[days_id] + "/Test_Data.bin"

    print(f"Getting route from stop {start_stop} to stop {destination_stop} starting at {start_time} minutes on {days_names[days_id]}", flush=True)
    # with open(stop_path, 'rb') as stop_file, open(trip_path, 'rb') as trip_file, open(schedule_path, 'rb') as schedule_file:
        # header_info.update(read_stop_data_header(stop_file))
        # header_info.update(read_trip_data_header(trip_file))
    schedule_data = []
    with open(schedule_path, 'rb') as schedule_file:
        print("Reading schedule data...", flush=True)
        header_info.update(read_schedule_data_header(schedule_file))
        print("Schedule header info:", header_info, flush=True)
        schedule_data = read_schedule_line(schedule_file, start_stop, start_time, header_info)
        print("Schedule data read: ", schedule_data, flush=True)
    raw_route = find_route(schedule_data, start_stop, destination_stop)
    print("Raw route found:", raw_route, flush=True)

    with open(stop_path, 'rb') as stop_file, open(trip_path, 'rb') as trip_file:
        print("Decoding route...", flush=True)
        route = decode_route(raw_route, stop_file, trip_file)
        print("Route decoded.", flush=True)
    # print(route['stops'][0])
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


if __name__ == "__main__":
    # get_route(1749, 2324, 480, 0)
    get_route(1, 2, 0, 0)