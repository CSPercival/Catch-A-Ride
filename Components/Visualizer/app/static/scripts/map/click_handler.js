import { map, addMarker } from './state_handler.js';
import { updateInvalidAddress } from '../form/input_handler.js';
// var map = L.map('map').setView([51.109603609969334, 17.032424849065997], 13); // Centered on London
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// var points = [];
// var routeLayer;
// var curr_marker = null;

map.on('click', function(e) {
    console.log("Map clicked at:", e.latlng);
    updateInvalidAddress(e.latlng);
    // addMarker(e.latlng.lat, e.latlng.lng, "Clicked Location");
    // Update form...?

    // if (points.length >= 2) {
    //     // Reset if we already have two points
    //     points = [];
    //     if (routeLayer) map.removeLayer(routeLayer);
    // }

    // var latlng = e.latlng;
    // // console.log(latlng)
    // points.push(latlng);
    // if(curr_marker != null){
    //     curr_marker.remove()
    // }
    // curr_marker = L.marker(latlng).addTo(map);

    // if (points.length === 2) {
    //     var start = `${points[0].lng},${points[0].lat}`;
    //     var end = `${points[1].lng},${points[1].lat}`;

    //     // Ask our Python backend for the route
    //     fetch(`/get_route?start=${start}&end=${end}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             var route = data.routes[0].geometry;
    //             routeLayer = L.geoJSON(route, {style: {color: 'blue', weight: 5}}).addTo(map);
    //         });
    // }
});