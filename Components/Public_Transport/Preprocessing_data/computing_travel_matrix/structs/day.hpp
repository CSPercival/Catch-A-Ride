#pragma once

#include "../../shared_structs/day.hpp"
#include <nlohmann/json.hpp>

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Day,
    id,
    variant,
    name
)