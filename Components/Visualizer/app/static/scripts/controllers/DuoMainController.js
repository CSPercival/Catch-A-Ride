import { mainEventBus } from './../EventBus.js'

function formToMapKey(formKey){
    return formKey.replace(/address/i, "Marker");
}

export class MainController{
    constructor(form, map){
        this.form = form
        this.map = map

        mainEventBus.addEventListener('mapClick', e => 
            this.handleMapClick(e)
        );

        mainEventBus.addEventListener('FormAddressChange', e => 
            this.handleFormAddressChange(e.detail)
        );

        mainEventBus.addEventListener('FormSubmit', e => 
            // console.log('Form Submit:', e.detail);
            this.handleFormSubmit(e.detail)
        );
    }

    handleMapClick(event){
        this.form.updateInvalidAddress(event.detail.lat + ", " + event.detail.lng);
    }

    handleFormAddressChange(event){
        this.map.clearPolylines();
        if(event.data.valid){
            this.map.crucialMarkerUpdate(formToMapKey(event.formKey), event.data.lat, event.data.lng, event.data.name);
        } else {
            this.map.clearCrucialMarker(formToMapKey(event.formKey));
        }
    }

    handleFormSubmit(event){
        console.log(event);
        fetch(window.APP_CONFIG.submitFormUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(event)
          })
          .then(res => res.json())
          .then(data => {
            handleBackendOrders(data);
          });
    }
}