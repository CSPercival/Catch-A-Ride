function addressTargetToKey(target){
    // console.log(target.id);
    const formKey = target.id === "car-start-address" ? "carStartAddress" : 
                    target.id === "pt-start-address" ? "ptStartAddress" : 
                    target.id === "finish-address" ? "finishAddress" :  
                    target.id === "meeting-address" ? "meetingAddress" :  
                    "UnknownAddress";
    return formKey;
}
function timeTargetToKey(target){
    // console.log(target.id);
    const formKey = target.id === "car-start-time" ? "carStartTime" : 
                    target.id === "pt-start-time" ? "ptStartTime" : 
                    "UnknownTime";
    return formKey;
}


export class FormController {
    constructor(view, state, mainEventBus,formEventBus){
        this.formEventBus = formEventBus;
        this.mainEventBus = mainEventBus;
        this.view = view;
        this.state = state;

        this.state.setAddressPresence(this.view.getPresentAddressKeys())

        formEventBus.addEventListener('FormAddressChange', e => 
            this.handleFormAddressChange(addressTargetToKey(e.detail.target), e.detail.target.value));
        formEventBus.addEventListener('FormTimeChange', e => 
            this.handleFormTimeChange(timeTargetToKey(e.detail.target), e.detail.target.value));
        formEventBus.addEventListener('FormStrategyChange', e => 
            this.handleFormStrategyChange(e));
        formEventBus.addEventListener('FormSubmit', e => this.handleFormSubmit(e));
    }

    handleFormAddressChange(formKey, newValue){
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
                this.mainEventBus.dispatchEvent(
                    new CustomEvent('FormAddressChange',{ 
                                                            detail: {
                                                                data : data,
                                                                formKey : formKey
                                                            }
                                                        }));
        });
    };

    handleFormTimeChange(formKey, newValue){
        this.state.updateTime(formKey, newValue);
        this.mainEventBus.dispatchEvent(
            new CustomEvent('FormTimeChange',   { detail :  {
                                                                data : newValue,
                                                                formKey : formKey
                                                            }
                                                }));
    };

    handleFormStrategyChange(event){
        this.state.flipStrategy();
        this.view.flipStrategy();
    };

    handleFormSubmit(event){
        console.log('Form Submitted:', event.detail);
        event.preventDefault();
        this.mainEventBus.dispatchEvent(new CustomEvent('FormSubmit', { detail: this.state.getState() }));
        alert("Form submitted successfully!");
    };

    updateInvalidAddress(new_place){
        const invalidKey = this.state.getInvalidAddressKey();
        if (invalidKey) {
            this.view.updateAddress(invalidKey, new_place);
            this.handleFormAddressChange(invalidKey, new_place);
        }
    }

}