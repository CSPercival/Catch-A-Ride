import { MapView } from './MapView.js';
import { MapEvents } from './MapEvents.js';
import { MapState } from './MapState.js';
import { MapController } from './MapController.js';

export class MapComponent {
    constructor(mapInstance){
        this.state = new MapState();
        this.view = new MapView(mapInstance);
        this.events = new MapEvents(this.view);
        this.controller = new MapController(this.view, this.state);
    }

    addCommonMarker(lat, lng, popupContent){
        this.controller.addCommonMarker(lat, lng, popupContent);
    }

    clearCommonMarkers(){
        this.controller.clearCommonMarkers();
    }

    crucialMarkerUpdate(whichMarker, lat, lng, popupContent){
        this.controller.crucialMarkerUpdate(whichMarker, lat, lng, popupContent);
    }

    clearCrucialMarker(){
        this.controller.clearCrucialMarker();
    }

    clearCrucialMarkers(){
        this.controller.clearCrucialMarkers();
    }

    addPolyline(latlngs, options, popupContent){
        this.controller.addPolyline(latlngs, options, popupContent);
    }

    clearPolylines(){
        this.controller.clearPolylines();
    }

    showAll(){
        this.controller.showAll();
    }
}