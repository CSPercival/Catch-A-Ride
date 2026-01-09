export const map = L.map('map').setView([51.109603609969334, 17.032424849065997], 13); // Centered on London
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const namePrefixes = {
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
    console.log("Adding ", popupContent," marker at:", lat, lng);
    let marker = L.marker([lat, lng], {title: popupContent}).addTo(map);
    marker.bindPopup(popupContent);
    return marker
}

function _removeMarker(marker){
    marker.remove();
}

export function addMarker(lat, lng, popupContent){
    mapState.commonLandmarks.push(_addMarker(lat, lng, popupContent));
}

export function updateCrucialMarker(lat, lng, name, whichMarker){
    if(mapState.crucialLandmarks[whichMarker] != null){
        _removeMarker(mapState.crucialLandmarks[whichMarker]);
    }

    mapState.crucialLandmarks[whichMarker] = _addMarker(lat, lng, namePrefixes[whichMarker] + name);
}