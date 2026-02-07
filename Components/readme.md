# Components

This directory contains the main building blocks of the system.  
Each component is responsible for a distinct part of the overall functionality
## Components Overview

### Map Service
Provides access to road network data and car routing functionality.  
It is responsible for computing travel times and routes for car-based transportation, including matrix and isochrone queries.

This component is based on **OpenRouteService (ORS)** and **OpenStreetMap (OSM)** data.

---

### Public Transport Service
Implements a custom routing engine for public transportation based on GTFS data.  
It supports advanced queries such as:
- travel time computation between multiple origins and destinations,
- route reconstruction,
- time-dependent queries,
- public transport isochrones.

The service relies heavily on preprocessing to ensure fast query response times during runtime.

---

### Meeting Point Service
Contains the core logic for determining the optimal meeting point between a car driver and a public transport passenger.

This component implements and compares multiple strategies, including:
- a discrete strategy based on public transport stops,
- a continuous strategy based on isochrone intersections.

Its output is an optimal meeting location.

---

### Visualizer
A lightweight web-based interface used to present the results of the computations.

The visualizer displays:
- the selected meeting point,
- individual travel routes,
- intermediate segments of the journey on an interactive map.