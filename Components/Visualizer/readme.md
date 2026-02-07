# Visualizer

The Visualizer is a lightweight web application built using the **Flask** framework.  
Its primary purpose is to present the results produced by the system in a clear and interactive way.

---

## Overview

The application exposes a **single view**, which allows the user to:
- provide input for a query
- visualize the computed meeting point
- display travel routes for both participants

The Visualizer is intended mainly as a **demonstration and debugging tool**, not as a full-featured end-user application.

---

## Map Visualization

All map-related rendering is implemented using the **Leaflet** JavaScript library.

Leaflet is used to:
- display the base map
- render routes and polylines
- mark start points, meeting points, and destinations

---

## Notes

The Visualizer focuses on simplicity and clarity.  
It does not provide advanced user interface features such as alternative route selection or detailed interaction controls, as these aspects are outside the scope of the project.
