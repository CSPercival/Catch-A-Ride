# Catch-A-Ride

This project is a prototype system for **synchronizing car travel with public transportation** in order to minimize the total travel time of two people heading towards a common destination.

Given:
- the starting location and time of a car driver,
- the starting location and time of a public transport passenger,
- a shared destination,

the system determines whether it is beneficial for the two people to meet along the way and continue the journey together, and if so, **where the optimal meeting point should be**.

The solution is based on real road network data and public transport timetables for the Wrocław metropolitan area.  
The application was developed as part of a bachelor’s thesis and is intended as a **research prototype**, not a production-ready system.

---

## Requirements

To run the project locally, the following tools are required:

- **Docker**
- **Git LFS (Large File Storage)** — required because some data files are large and tracked using Git LFS

Before cloning the repository, make sure Git LFS is installed and initialized:

```bash
git lfs install
git clone <repository-url>
```

---

## Setup

Ensure that Docker is installed and running on your system.

Prepare the Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Application

Start the application using:

```bash
python3 main.py
```

After startup, the application will be available at:

```
http://127.0.0.1:5000
```

---

## Notes

- The first startup may take longer due to complex preprocessing process.
- The system relies on static models of traffic and public transport schedules.
- The web interface is intended mainly for visualization and demonstration purposes.

--

## Data Sources and Attribution

This project makes use of the following open data and services:

- **OpenStreetMap (OSM)**  
  © OpenStreetMap contributors  
  Data available under the Open Database License (ODbL):  
  https://www.openstreetmap.org/copyright

- **OpenRouteService (ORS)**  
  Routing and geocoding services provided by Heidelberg Institute for Geoinformation Technology (HeiGIT)  
  https://openrouteservice.org/

The data and services are used in accordance with their respective licenses.
