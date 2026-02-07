# Meeting Point Service

The Meeting Point Service is the core decision-making component of the system.  
It combines results from the **Map Service** and the **Public Transport Service** to determine an optimal meeting location for a car driver and a public transport passenger.

The goal of this service is to minimize the total travel time to the final destination or decide that traveling separately is the better option.

---

## Meeting Point Strategies

The service implements **two alternative strategies** for finding a meeting point:

### Discrete Strategies

First strategy operates on a **discrete set of candidate meeting locations**.  
In these approaches, the search space is limited to a predefined collection of points (stops and starting locations of both individuals), which allows for predictable performance and simpler evaluation.

### Isochrone-Based Strategy

Second strategy operates on a **continuous spatial domain** and is based on **isochrone intersections**.

In this approach:
- reachable areas for both participants are computed independently,
- intersections of these areas are identified,
- candidate meeting locations are derived from the overlapping regions.

This strategy is more flexible and can yield higher-quality results, but is also computationally more demanding.
