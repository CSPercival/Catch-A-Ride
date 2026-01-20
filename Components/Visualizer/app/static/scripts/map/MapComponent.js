import { MapView } from './MapView.js';
import { MapEvents } from './MapEvents.js';
import { MapState } from './MapState.js';
import { MapController } from './MapController.js';
import { mainEventBus } from '../EventBus.js';

export class MapComponent {
    constructor(mapInstance){
        this.state = new MapState();
        this.view = new MapView(mapInstance);
        this.events = new MapEvents(this.view, mainEventBus);
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

    clearCrucialMarker(whichMarker){
        this.controller.clearCrucialMarker(whichMarker);
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