var map = L.map('map').setView([51.109603609969334, 17.032424849065997], 13); // Centered on London
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

var points = [];
var routeLayer;
var curr_marker = null;

map.on('click', function(e) {
    if (points.length >= 2) {
        // Reset if we already have two points
        points = [];
        if (routeLayer) map.removeLayer(routeLayer);
    }

    var latlng = e.latlng;
    points.push(latlng);
    if(curr_marker != null){
        curr_marker.remove()
    }
    curr_marker = L.marker(latlng).addTo(map);

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