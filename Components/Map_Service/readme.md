# Map Service

The Map Service is responsible for all road-network–based operations in the system, including car routing, travel time computation, and isochrone generation.

It operates on a **local instance of OpenRouteService (ORS)** running inside a Docker container and uses **OpenStreetMap (OSM)** data as the underlying road network.

---

## Architecture Overview

The service is split into two main client classes:

### ORSClient
Handles all interactions with the local ORS instance, including:
- car routing queries,
- travel time and distance matrices,
- isochrone generation.

All routing and isochrone computations are performed **locally**, ensuring predictable performance and independence from external API rate limits.

---

### GeoClient
Responsible for geocoding and reverse geocoding operations (address ↔ coordinates).

Unlike routing, **geocoding is not performed locally** and relies on an external geocoding service.  
This design choice avoids the overhead of maintaining a separate local geocoding database while keeping routing fully self-hosted.

---

## Running OpenRouteService (ORS)

The Map Service requires a running local ORS instance provided via Docker.

### Starting ORS manually

To start the ORS service manually, navigate to the `ors-docker` directory and run:

```bash
docker compose up
```

Once started, the ORS API will be available at:
```bash
http://localhost:8085/ors
```

### First Startup Note

The first launch of the ORS Docker container may take a significant amount of time.

This is due to the **preprocessing of routing graphs** based on the provided OpenStreetMap data.  
Depending on the size of the map and available hardware resources, this step may take several minutes.

Once preprocessing is complete, subsequent startups are significantly faster.