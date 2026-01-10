#pragma once

#include "../../shared_structs/stops.hpp"
#include <nlohmann/json.hpp>

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Stop,
    id,
    old_id,
    name,
    lat,
    lng
)

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Stops,
    number_of_stops,
    id_mapping,
    name_mapping,
    stops
)