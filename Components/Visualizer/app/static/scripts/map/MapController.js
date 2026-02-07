const markerNamePrefixes = {
    carStartMarker : "Starting point (car): ",
    ptStartMarker : "Starting point (public transport): ",
    finishMarker : "Destination: ",
    meetingMarker : "Meeting point: "
};
// car_color = "#3b82f6"
    // pt_color = "#8b5cf6" 
    // duo_color = "#10b981"
const markerIconOptions = {
    carStartMarker : {
                        icon: 'car',
                        iconShape: 'marker',
                        borderColor: '#2d3436',
                        textColor: '#2d3436',
                        backgroundColor: '#3b82f6'
                     },
    ptStartMarker : {
                        icon: 'bus',
                        iconShape: 'marker',
                        borderColor: '#2d3436',
                        textColor: '#2d3436',
                        backgroundColor: '#8b5cf6'
                     },
    finishMarker : {
                        icon: 'flag-checkered',
                        iconShape: 'marker',
                        borderColor: '#2d3436',
                        textColor: '#2d3436',
                        backgroundColor: '#10b981'
                     },
    meetingMarker : {
                        icon: 'bullseye',
                        iconShape: 'marker',
                        borderColor: '#2d3436',
                        textColor: '#2d3436',
                        backgroundColor: '#f97316'
                     }
}

export class MapController {
    constructor(view, state){
        this.view = view;
        this.state = state;
    }

    addCommonMarker(lat, lng, popupContent){
        let marker = this.view.addMarker(lat, lng, popupContent);
        this.state.addCommonMarker(marker);
    }

    clearCommonMarkers(){
        this.view.removeMarkers(this.state.commonMarkers);
        this.state.clearCommonMarkers();
    }

    crucialMarkerUpdate(whichMarker, lat, lng, popupContent){
        let existingMarker = this.state.getCrucialMarker(whichMarker);
        if(existingMarker != null){
            this.view.removeMarker(existingMarker);
        }
        let newMarker = this.view.addMarker(lat, lng, markerNamePrefixes[whichMarker] + popupContent, markerIconOptions[whichMarker]);
        this.state.updateCrucialMarker(whichMarker, newMarker);
    }

    clearCrucialMarker(whichMarker){
        let marker = this.state.getCrucialMarker(whichMarker);
        if(marker != null){
            this.view.removeMarker(marker);
        }
        this.state.updateCrucialMarker(whichMarker, null);
    }

    clearCrucialMarkers(){
        Object.keys(this.state.crucialMarkers).forEach(whichMarker => {
            let marker = this.state.getCrucialMarker(whichMarker);
            if(marker != null){
                this.view.removeMarker(marker);
            }
        });
        this.state.clearCrucialMarkers();
    }

    addPolyline(latlngs, options, popupContent){
        let polyline = this.view.addPolyline(latlngs, options, popupContent);
        this.state.addPolyline(polyline);
    }

    clearPolylines(){
        this.view.removePolylines(this.state.polylines);
        this.state.clearPolylines();
    }

    showAll(){
        this.view.showAll(this.state.getState());
    }
}