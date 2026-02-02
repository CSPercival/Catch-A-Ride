import { mainEventBus } from './../EventBus.js'

function formToMapKey(formKey){
    return formKey.replace(/address/i, "Marker");
}

export class MainController{
    constructor(form, map, timeline){
        this.form = form;
        this.map = map;
        this.timeline = timeline;

        mainEventBus.addEventListener('mapClick', e => 
            this.handleMapClick(e)
        );

        mainEventBus.addEventListener('FormAddressChange', e => 
            this.handleFormAddressChange(e.detail)
        );

        mainEventBus.addEventListener('FormTimeChange', e => 
            this.handleFormTimeChange(e.detail)
        );

        mainEventBus.addEventListener('FormSubmit', e => 
            this.handleFormSubmit(e.detail)
        );
    }

    handleMapClick(event){
        this.form.updateInvalidAddress(event.detail.lat + ", " + event.detail.lng);
    }

    handleFormAddressChange(event){
        this.timeline.clearTimelines();
        this.map.clearPolylines();
        this.map.clearCrucialMarker("meetingMarker");
        if(event.data.valid){
            this.map.crucialMarkerUpdate(formToMapKey(event.formKey), event.data.lat, event.data.lng, event.data.name);
        } else {
            this.map.clearCrucialMarker(formToMapKey(event.formKey));
        }
        this.map.showAll();
    }

    handleFormTimeChange(event){
        this.timeline.clearTimelines();
        this.map.clearPolylines();
        this.map.clearCrucialMarker("meetingMarker");
        this.map.showAll();
    }

    handleFormSubmit(event){
        fetch(window.APP_CONFIG.submitFormUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(event)
          })
          .then(res => res.json())
          .then(data => {
            this.handleBackendOrders(data);
          });
    }

    handleBackendOrders(orders){
        this.handleMapOrders(orders.map);
        this.handleInfoOrders(orders.timeline);
    }

    handleMapOrders(orders){
        console.log("MAP HANDLING",orders);
        
        if(orders.clearCommonMarkers) this.map.clearCommonMarkers();
        if(orders.clearPolylines) this.map.clearPolylines();

        orders.markersToAdd.forEach(marker => {
            this.map.addCommonMarker(marker.lat, marker.lng, marker.popupContent);
        });
        
        Object.keys(orders.mainMarkers).forEach(key =>{
            this.map.crucialMarkerUpdate(key, orders.mainMarkers[key].lat, orders.mainMarkers[key].lng, orders.mainMarkers[key].name)
        });

        orders.polylinesToAdd.forEach(polylineData => {
            const routeCoordinates = polyline.decode(polylineData.geometry, 5);
            routeCoordinates.forEach(coord => { coord = [coord[1], coord[0]]; });
            this.map.addPolyline(routeCoordinates, polylineData.options, polylineData.popupContent);
        });
        this.map.showAll();
    }

    handleInfoOrders(orders){
        console.log("ROUTE INFO", orders);
        this.timeline.handleOrders(orders);
    }
}