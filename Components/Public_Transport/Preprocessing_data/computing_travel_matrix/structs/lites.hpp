#pragma once

#include "../../shared_structs/lites.hpp"
#include <nlohmann/json.hpp>

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    Vertex_lite,
    stop,
    time
)