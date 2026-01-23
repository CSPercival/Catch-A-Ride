from Components.Map_Service.mapors_getters import single_geometry
import random

class MapOrders:
    def __init__(self):
        self.eps = 1/1000

        self.clearCommonMarkers = True
        self.clearPolylines = True
        self.mainMarkers = {}
        self.markersToAdd = []
        self.polylinesToAdd = []

        self.colors = [
            "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", 
            "black", "blue", "blueviolet", "brown", "burlywood", "cadetblue", 
            "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", 
            "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkgrey", 
            "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", 
            "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey", 
            "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey", 
            "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro", 
            "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "grey", 
            "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", 
            "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan", 
            "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink", 
            "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey", 
            "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", 
            "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", 
            "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", 
            "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", 
            "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", 
            "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", 
            "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "purple", 
            "rebeccapurple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon", 
            "sandybrown", "seagreen", "sienna", "silver", "skyblue", "slateblue", 
            "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "teal", 
            "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", 
            "yellow", "yellowgreen"
        ]
        # white: "seashell", "lavenderblush", 
        # kremowe: "navajowhite", "blanchedalmond",

    def clear_orders(self):
        self.clearCommonMarkers = True
        self.clearPolylines = True
        self.mainMarkers = {}
        self.markersToAdd = []
        self.polylinesToAdd = []
    
    def get_orders(self):
        map_orders = {
            "clearCommonMarkers" : self.clearCommonMarkers,
            "clearPolylines": self.clearPolylines,
            "mainMarkers" : self.mainMarkers,
            "markersToAdd" : self.markersToAdd,
            "polylinesToAdd" : self.polylinesToAdd
        }
        return map_orders
    
    def main_marker_update(self, coordinate, name, which_marker):
        new_marker = {
            "lat": coordinate[0],
            "lng": coordinate[1],
            "name": name
        }
        self.mainMarkers[which_marker] = new_marker

    def add_marker(self, coordinate, popup_content):
        new_marker = {
            "lat": coordinate[0],
            "lng": coordinate[1],
            "popupContent": popup_content
        }
        for marker in self.markersToAdd:
            if(abs(marker['lat'] - new_marker['lat']) < self.eps):
                if(abs(marker['lng'] - new_marker['lng']) < self.eps):
                    marker['popupContent'] += "\n" + new_marker['popupContent']
                    return
        self.markersToAdd.append(new_marker)

    def add_walk(self, ors_walk_responce, popup_content):
        random_color = random.choice(self.colors)
        new_polyline = {
            "geometry": single_geometry(ors_walk_responce),
            "options": {
                "color": random_color,
                "dashArray" : '10, 10'
            },
            "popupContent": popup_content + random_color
        }
        self.polylinesToAdd.append(new_polyline)

    def add_car(self, ors_drive_responce, popup_content):
        random_color = random.choice(self.colors)
        new_polyline = {
            "geometry": single_geometry(ors_drive_responce),
            "options": {
                "color": random_color,
            },
            "popupContent": popup_content + random_color
        }
        self.polylinesToAdd.append(new_polyline)
        