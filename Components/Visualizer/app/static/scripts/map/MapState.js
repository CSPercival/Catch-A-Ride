export class MapState {
    constructor(){
        this.crucialMarkers = {
            carStartMarker : null,
            ptStartMarker : null,
            finishMarker : null,
            meetingMarker : null
        };
        this.commonMarkers = [];
        this.polylines = [];
        this.polygons = [];
    }

    getCrucialMarker(whichMarker){
        return this.crucialMarkers[whichMarker];
    }

    getCrucialMarkers(){
        return this.crucialMarkers;
    }

    getCommonMarkers(){
        return this.commonMarkers;
    }

    getPolylines(){
        return this.polylines;
    }

    getPolygons(){
        return this.polygons;
    }

    getState(){
        return {
            crucialMarkers: this.crucialMarkers,
            commonMarkers: this.commonMarkers,
            polylines: this.polylines,
            polygons: this.polygons
        };
    }

    addCommonMarker(marker){
        this.commonMarkers.push(marker);
    }

    updateCrucialMarker(whichMarker, marker){
        this.crucialMarkers[whichMarker] = marker;
    }

    addPolyline(polyline){
        this.polylines.push(polyline);
    }

    clearCrucialMarkers(){
        this.crucialMarkers = {
            carStartMarker : null,
            ptStartMarker : null,
            finishMarker : null,
            meetingMarker : null
        };
    }

    clearCommonMarkers(){
        this.commonMarkers = [];
    }

    clearPolylines(){
        this.polylines = [];
    }

}