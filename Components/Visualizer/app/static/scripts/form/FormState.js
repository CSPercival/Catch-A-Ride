export class FormState {
    constructor(){
        this.addresses = {
            carStartAddress: {
                name : "",
                lat : 0.0,
                lng : 0.0,
                valid : false,
                locked : false,
                present: false
            },
            ptStartAddress: {
                name : "",
                lat : 0.0,
                lng : 0.0,
                valid : false,
                locked : false,
                present: false
            },
            finishAddress: {
                name : "",
                lat : 0.0,
                lng : 0.0,
                valid : false,
                locked : false,
                present: false
            },
            meetingAddress: {
                name : "",
                lat : 0.0,
                lng : 0.0,
                valid : false,
                locked : true,
                present: false
            }
        };
        this.times = {
            ptStartTime : {
                displayedString : "",
                hour : 0,
                minute : 0,
                valid: false
            },
            carStartTime : {
                displayedString : "",
                hour : 0,
                minute : 0,
                valid: false
            }
        }
    }

    setAddressPresence(presentAddressKeys){
        Object.keys(this.addresses).forEach( key =>
            this.addresses[key].present = presentAddressKeys.includes(key)
        )
    }

    updateAddress(key, name=null, lat=null, lng=null, valid=null, locked=null){
        if(this.addresses.hasOwnProperty(key)){
            name ??= this.addresses[key].name;
            lat ??= this.addresses[key].lan;
            lng ??= this.addresses[key].lng;
            valid ??= this.addresses[key].valid;
            locked ??= this.addresses[key].locked;
            this.addresses[key] = {
                name: name,
                lat: lat,
                lng: lng,
                valid: valid,
                locked: locked,
                present: true
            };
        } else {
            console.log("UPDATE FORM STATE ERROR: unknown key:", key)
        }
    }

    getState(){
        return {
            addresses : this.addresses,
            times : this.times
        }
    }

    getInvalidAddressKey(){
        const invalidKey = Object.keys(this.addresses).find(
            (key) => this.addresses[key].valid === false && 
                    this.addresses[key].present && 
                    !this.addresses[key].locked 
        );
        return invalidKey;
    }
}