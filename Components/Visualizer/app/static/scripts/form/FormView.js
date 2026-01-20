export class FormView {
    constructor(){
        this.addresses = {
            carStartAddress: {
                input : document.getElementById("car-start-address"),
                feedback : document.getElementById("car-start-address-feedback")
            },
            ptStartAddress: {
                input : document.getElementById("pt-start-address"),
                feedback : document.getElementById("pt-start-address-feedback")
            },
            finishAddress: {
                input : document.getElementById("finish-address"),
                feedback : document.getElementById("finish-address-feedback")
            },
            meetingAddress: {
                input : document.getElementById("meeting-address"),
                feedback : document.getElementById("meeting-address-feedback")
            },
        };
        this.times = {
            carStartTime: {
                input : document.getElementById("car-start-time"),
                feedback : document.getElementById("car-start-time-feedback")
            },
            ptStartTime: {
                input : document.getElementById("pt-start-time"),
                feedback : document.getElementById("pt-start-time-feedback")
            }
        }
        this.submitButton = document.getElementById("form-submit-button")
    }

    getPresentAddressKeys(){
        return Object.keys(this.addresses).filter(key => this.addresses[key].input);
    }

    updateAddress(key, name, feedback = "", valid = 1){
        if(this.addresses.hasOwnProperty(key)){
            this.addresses[key].feedback.textContent = feedback;
            this.addresses[key].feedback.style.color = valid ? "green" : "red";
            this.addresses[key].input.value = name;
        } else {
            console.log("udpateAddress FORM VIEW ERROR: unknown key: ", key);
        }
    }

    setAsWaiting(key){
        if(this.addresses.hasOwnProperty(key)){
            this.addresses[key].feedback.textContent = "Validating...";
            this.addresses[key].feedback.style.color = "orange";
        } else {
            console.log("setAsWaiting FORM VIEW ERROR: unknown key: ", key);
        }
    }

    bindAddressChangeEvent(handler){
        for(let key in this.addresses){
            if(this.addresses[key].input){
                this.addresses[key].input.addEventListener("change", handler);
            }
        }
    }

    bindTimeChangeEvent(handler){
        for(let key in this.times){
            if(this.times[key].input){
                this.times[key].input.addEventListener("change", handler);
            }
        }
    }

    bindSubmitEvent(handler){
        this.submitButton.addEventListener("click", handler);
    }
}