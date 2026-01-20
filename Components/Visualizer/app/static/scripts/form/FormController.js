function targetToKey(target){
    console.log(target.id);
    const formKey = target.id === "car-start-address" ? "carStartAddress" : 
                    target.id === "pt-start-address" ? "ptStartAddress" : 
                    target.id === "finish-address" ? "finishAddress" :  
                    target.id === "meeting-address" ? "meetingAddress" :  
                    "UnknownAddress";
    return formKey;
}


export class FormController {
    constructor(view, state, mainEventBus,formEventBus){
        this.formEventBus = formEventBus;
        this.mainEventBus = mainEventBus;
        this.view = view;
        this.state = state;

        this.state.setAddressPresence(this.view.getPresentAddressKeys())

        formEventBus.addEventListener('FormAddressChange', 
            e => this.handleFormAddressChange(targetToKey(e.detail.target), e.detail.target.value));
        formEventBus.addEventListener('FormTimeChange', e => this.handleFormTimeChange(e));
        formEventBus.addEventListener('FormSubmit', e => this.handleFormSubmit(e));
    }

    handleFormAddressChange(formKey, newValue){
        // console.log('Address changed:', event.detail);
        // const target = event.detail.target
        // const newValue = target.value
        // const formKey = target === "input#car-start-address" ? "carStartAddress" : 
        //                 target === "input#pt-start-address" ? "ptStartAddress" : 
        //                 target === "input#finish-address" ? "finishAddress" :  
        //                 "meetingAddress";
        this.view.setAsWaiting(formKey);
        fetch(window.APP_CONFIG.validateAddressUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ address: newValue })
            })
            .then(res => res.json())
            .then(data => {
                this.state.updateAddress(formKey, data.name, data.lat, data.lng, data.valid);
                this.view.updateAddress(formKey, data.name, data.message, data.valid);
                this.mainEventBus.dispatchEvent(new CustomEvent('FormAddressChange', { 
                                                                            detail: {
                                                                                data : data,
                                                                                formKey : formKey
                                                                            }
                                                                        }));
        });
    };

    handleFormTimeChange(event){
        console.log('Time changed:', event.detail);
    };

    handleFormSubmit(event){
        console.log('Form Submitted:', event.detail);
        event.preventDefault();
        this.mainEventBus.dispatchEvent(new CustomEvent('FormSubmit', { detail: this.state.getState() }));
        alert("Form submitted successfully! XD");
    };

    updateInvalidAddress(new_place){
        const invalidKey = this.state.getInvalidAddressKey();
        if (invalidKey) {
            this.view.updateAddress(invalidKey, new_place);
            this.handleFormAddressChange(invalidKey, new_place);
        }
    }

}