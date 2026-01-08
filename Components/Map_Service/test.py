from ors_client import ORSClient
from map_client import MapClient
import json

ors = ORSClient(profile='driving-car')
geo = MapClient()

swiebodzki_c = (17.020325415863713, 51.108029811174276)
swiebodzki_n = "Dworzec Świebodzki, Wrocław, Poland"
dominikanska_c = (17.039332035410443, 51.108121831727026)
dominikanska_n = "Galeria Dominikańska, Wrocław"

plac_dominikanski_n = "Plac Dominikański"

zlotnicka_c = (16.889998009694054, 51.14375935425375)
ii_c = (17.053214096034708, 51.1109046846232)


# data = ors.simple_path([swiebodzki_c, dominikanska_c])
# print(data)


# data = geo.geocode(swiebodzki_n)
# print(json.dumps(data, indent=4))
# data = geo.geocode(plac_dominikanski_n)
# print(json.dumps(data, indent=4))
print(geo.validate_coordinates(swiebodzki_c))
print(geo.validate_coordinates(zlotnicka_c))
print(geo.validate_coordinates(ii_c))
print(geo.validate_coordinates(dominikanska_c))

# data = geo.reverse_geocode(swiebodzki_c)
# print(json.dumps(data, indent=4))
# data = geo.reverse_geocode(dominikanska_c)
# print(json.dumps(data, indent=4))
