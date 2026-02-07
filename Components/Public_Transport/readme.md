# Public Transport Service

The Public Transport Service is a custom-built routing engine for public transportation, designed specifically for this project.

Unlike external APIs, this module is implemented **from scratch** and operates on **real-world public transport data** (GTFS timetables).  
Routing queries are answered using a **time-dependent variant of Dijkstra’s algorithm**, adapted to the structure of public transport networks.

---

## Preprocessing

All routing results are generated during a **preprocessing stage** and stored on disk.

- preprocessing must be rerun **every time the timetable data changes**,
- the process is **computationally expensive** and time-consuming,
- it requires significant disk space for storing generated data structures,
- once completed, runtime queries are reduced mostly to fast disk reads.

---

## PTClient Interface

The service exposes its functionality through the `PTClient` class, which provides the following methods:

- `arrival_time_stop(u_id, v_id, m)`  
  Returns the earliest possible arrival time at stop `v_id` when departing from stop `u_id` at time `m`.

- `arrival_time_stop_vector(U_id, V_id, M)`  
  Batch version of the basic query. For multiple start stops `U_id` and corresponding start times `M`, returns the minimal arrival time to each stop in `V_id`.

- `arrival_times_vector(u_coords, V_id, m)`  
  For a geographic start location and departure time `m`, returns the shortest travel times to all stops in `V_id`.

- `arrival_time(u_coords, v_coords, m)`  
  Returns the shortest total travel time between two geographic locations, starting at time `m`.

- `route(u_coords, v_coords, m)`  
  Returns a detailed description of the optimal route, including walking segments, intermediate stops, and transit line numbers.

- `isochrones(U_id, M, m')`  
  For each stop in `U_id` and its corresponding start time, returns the area that is reachable on foot up to time `m'`.
