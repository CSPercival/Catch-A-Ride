from flask import Flask, render_template, request, jsonify
import requests

brain = Flask(__name__)

@brain.route('/')
def index():
    return render_template('index.html')

@brain.route('/get_route')
def get_route():
    # Get coordinates from the frontend request
    start_coords = request.args.get('start') # format: "lng,lat"
    end_coords = request.args.get('end')     # format: "lng,lat"

    # Call the free OSRM API
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_coords};{end_coords}?overview=full&geometries=geojson"
    
    response = requests.get(osrm_url)
    data = response.json()
    print(data)

    # Send the route data back to the frontend
    return jsonify(data)

if __name__ == '__main__':
    brain.run(debug=True)