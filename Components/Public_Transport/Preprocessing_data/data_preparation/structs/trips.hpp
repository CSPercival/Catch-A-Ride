#pragma once

#include "lites.hpp"
#include "day.hpp"
#include "../../shared_structs/trips.hpp"
#include <nlohmann/json.hpp>

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Trip,
    id,
    trip_type,
    old_id,
    line_name,
    route
)

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Trips,
    number_of_trips,
    day,
    id_mapping,
    line_name_mapping,
    trips
)