from Components.Map_Service.mapors_getters import single_duration

class SingleTimeLineOrders:
    def __init__(self, name):
        self.header = {
            "name": name
        }
        self.events = []
        self.clear_time_line()

    def clear_time_line(self):
        self.header = {
            "name" : self.header['name'],
            "startTime": None,
            "finishTime": None,
            "duration" : None
        }
        self.events = []
    
    def set_header(self, start_time, finish_time):
        self.header['startTime'] = start_time
        self.header['finishTime'] = finish_time
        self.header['duration'] = (finish_time - start_time + 1440) % 1440
    
    def add_event(self, title, description, start_time, finish_time, color):
        event = {
            "title" : title,
            "description": description,
            "startTime": start_time,
            "finishTime": finish_time,
            "duration" : (finish_time - start_time + 1440) % 1440,
            "color" : color
        }
        self.events.append(event)
    
    def get_orders(self):
        return {
            "header": self.header,
            "events": self.events
        }

class TimelineOrders:
    def __init__(self):
        self.header = {}

        self.single_car = SingleTimeLineOrders("Single Car")
        self.single_pt = SingleTimeLineOrders("Single Public Transport")
        self.duo = SingleTimeLineOrders("Duo")

        self.clear_orders()

    def clear_orders(self):
        self.header = {
            'meetingPointName' : "",
            'journeyStartTime' : None,
            'journeyFinishTime' : None,
            'journeyDuration' : None,
        }
        self.single_car.clear_time_line()
        self.single_pt.clear_time_line()
        self.duo.clear_time_line()
    
    def get_orders(self):
        timeline_orders = {}
        timeline_orders['header'] = self.header
        if len(self.single_car.events) > 0:
            timeline_orders['car'] = self.single_car.get_orders()
        if len(self.single_pt.events) > 0:
            timeline_orders['pt'] = self.single_pt.get_orders()
        if len(self.duo.events) > 0:
            timeline_orders['duo'] = self.duo.get_orders()
        return timeline_orders

    def set_main_header(self, meeting_point_name, start_time, finish_time):
        self.header['meetingPointName'] = meeting_point_name
        self.header['journeyStartTime'] = start_time
        self.header['journeyFinishTime'] = finish_time
        self.header['journeyDuration'] = (finish_time - start_time + 1440) % 1440

    def get_single_timeline(self, key):
        if key == "car":
            return self.single_car
        elif key == "pt":
            return self.single_pt
        elif key == "duo":
            return self.duo
        else:
            return None

    def set_little_header(self, key, start_time, finish_time):
        single_timeline = self.get_single_timeline(key)
        if single_timeline == None:
            print("ERROR, Timeline update - unknown key", key)
            return
        single_timeline.set_header(start_time, finish_time)

    def add_pt(self, key, pt_segment, color = "red"):
        single_timeline = self.get_single_timeline(key)
        if single_timeline == None:
            print("ERROR, Timeline update - unknown key", key)
            return
        title_string = pt_segment['type'] + " " + pt_segment['line_name']
        title_string += ", " + pt_segment['route'][0]['name'] + " -> " + pt_segment['route'][-1]['name']
        desctiption_string = "Trip description\n subdescription"
        start_time = pt_segment['route'][0]['arrival_time']
        finish_time = pt_segment['route'][-1]['arrival_time']
        single_timeline.add_event(title_string, desctiption_string, start_time, finish_time, color)  


    def add_pt_walk(self, key, pt_segment, color = "blue"):
        single_timeline = self.get_single_timeline(key)
        if single_timeline == None:
            print("ERROR, Timeline update - unknown key", key)
            return
        title_string = "Walk"
        title_string += ": " + pt_segment['route'][0]['name'] + " -> " + pt_segment['route'][-1]['name']
        desctiption_string = "Walk description\n subdescription"
        start_time = pt_segment['route'][0]['arrival_time']
        finish_time = pt_segment['route'][-1]['arrival_time']
        single_timeline.add_event(title_string, desctiption_string, start_time, finish_time, color)

    def add_car(self, key, ors_car_responce, segment_start_time, color = "green"):
        single_timeline = self.get_single_timeline(key)
        if single_timeline == None:
            print("ERROR, Timeline update - unknown key", key)
            return
        title_string = "Car route to meeting place"
        # title_string += ": " + pt_segment['route'][0]['name'] + " -> " + pt_segment['route'][-1]['name']
        desctiption_string = "Car description\n subdescription"
        start_time = segment_start_time
        finish_time = segment_start_time + round(single_duration(ors_car_responce) / 60)
        single_timeline.add_event(title_string, desctiption_string, start_time, finish_time, color)
        