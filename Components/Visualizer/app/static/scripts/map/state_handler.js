export const map = L.map('map').setView([51.109603609969334, 17.032424849065997], 13); // Centered on London
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const landmarkNamePrefixes = {
    carLandmark : "Starting point (car): ",
    ptLandmark : "Starting point (public transport): ",
    finishLandmark : "Destination: "
};

const mapState = {
    crucialLandmarks: {
        carLandmark : null,
        ptLandmark : null,
        finishLandmark : null,
    },
    commonLandmarks: [],
    polylines: [],
    polygons : []
};

function _addMarker(lat, lng, popupContent){
    let marker = L.marker([lat, lng], {title: popupContent}).addTo(map);
    marker.bindPopup(popupContent);
    return marker
}

function _removeMarker(marker){
    marker.remove();
}

function _clearCommonMarkers(){
    mapState.commonLandmarks.forEach(marker => {_removeMarker(marker);});
    mapState.commonLandmarks = [];
}

function _addPolyline(latlngs, options, popupContent){
    let polyline = L.polyline(latlngs, options).addTo(map);
    polyline.bindPopup(popupContent);
    mapState.polylines.push(polyline);
    return polyline;
}

function _clearPolylines(){
    mapState.polylines.forEach(polyline => {polyline.remove();});
    mapState.polylines = [];
}

function _showAll(){
    const bounds = L.latLngBounds();
    Object.values(mapState.crucialLandmarks).forEach(marker => {
        if(marker != null){
            bounds.extend(marker.getLatLng());
        }
    });
    mapState.commonLandmarks.forEach(marker => {
        bounds.extend(marker.getLatLng());
    });
    mapState.polylines.forEach(polyline => {
        bounds.extend(polyline.getBounds());
    });
    map.fitBounds(bounds);
}

export function addMarker(lat, lng, popupContent){
    mapState.commonLandmarks.push(_addMarker(lat, lng, popupContent));
}

export function updateCrucialMarker(lat, lng, name, whichMarker){
    if(mapState.crucialLandmarks[whichMarker] != null){
        _removeMarker(mapState.crucialLandmarks[whichMarker]);
    }
    mapState.crucialLandmarks[whichMarker] = _addMarker(lat, lng, landmarkNamePrefixes[whichMarker] + name);
}

// data {
//     clearCommonLandmarks : Boolean
//     clearPolylines: Boolean
//     landmarksToAdd : [
//         {
//             lat: Number,
//             lng: Number,
//             popupContent: String
//         }
//     ]
//     polylinesToAdd : [
//         {
//             geometry: string,
//             options: {
//                 color: String,
//                 dashArra*: [Number]
//             },
//             popupContent: String
//         }        
//     ]
// }
export function handleBackendOrders(data){
    if(data.clearCommonLandmarks){
        _clearCommonMarkers();
    }
    if(data.clearPolylines){
        _clearPolylines();
    }
    data.landmarksToAdd.forEach(landmark => {
        _addMarker(landmark.lat, landmark.lng, landmark.popupContent);
    });
    data.polylinesToAdd.forEach(polylineData => {
        const routeCoordinates = polyline.decode(polylineData.geometry, 5);
        routeCoordinates.forEach(coord => { coord = [coord[1], coord[0]]; });
        _addPolyline(routeCoordinates, polylineData.options, polylineData.popupContent);
    });
    _showAll();
}