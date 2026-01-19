export class MapView {
    constructor(mapInstance){
        this.map = mapInstance;
    }

    addMarker(lat, lng, popupContent){
        let marker = L.marker([lat, lng], {title: popupContent}).addTo(this.map);
        marker.bindPopup(popupContent);
        return marker
    }
    
    removeMarker(marker){
        marker.remove();
    }

    removeMarkers(markers){
        markers.forEach(marker => {this.removeMarker(marker);});
    }
    
    addPolyline(latlngs, options, popupContent){
        let polyline = L.polyline(latlngs, options).addTo(this.map);
        polyline.bindPopup(popupContent);
        return polyline;
    }

    removePolyline(polyline){
        polyline.remove();
    }

    removePolylines(polylines){
        polylines.forEach(polyline => {this.removePolyline(polyline);});
    }
    
    showAll(mapState){
        const bounds = L.latLngBounds();
        Object.values(mapState.crucialMarkers).forEach(marker => {
            if(marker != null){
                bounds.extend(marker.getLatLng());
            }
        });
        mapState.commonMarkers.forEach(marker => {
            bounds.extend(marker.getLatLng());
        });
        mapState.polylines.forEach(polyline => {
            bounds.extend(polyline.getBounds());
        });
        this.map.fitBounds(bounds);
    }
    
    bindClickEvent(handler){
        this.map.on('click', handler);
    }
    // updateCrucialMarker(lat, lng, name, whichMarker){
    //     if(mapState.crucialLandmarks[whichMarker] != null){
    //         _removeMarker(mapState.crucialLandmarks[whichMarker]);
    //     }
    //     mapState.crucialLandmarks[whichMarker] = _addMarker(lat, lng, landmarkNamePrefixes[whichMarker] + name);
    // }
    
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
    // handleBackendOrders(data){
    //     if(data.clearCommonLandmarks){
    //         _clearCommonMarkers();
    //     }
    //     if(data.clearPolylines){
    //         _clearPolylines();
    //     }
    //     data.landmarksToAdd.forEach(landmark => {
    //         _addMarker(landmark.lat, landmark.lng, landmark.popupContent);
    //     });
    //     data.polylinesToAdd.forEach(polylineData => {
    //         const routeCoordinates = polyline.decode(polylineData.geometry, 5);
    //         routeCoordinates.forEach(coord => { coord = [coord[1], coord[0]]; });
    //         _addPolyline(routeCoordinates, polylineData.options, polylineData.popupContent);
    //     });
    //     _showAll();
    // }
}