export class FormEvents {
    constructor(view, formEventBus){
        this.view = view;
        this.formEventBus = formEventBus;

        this.view.bindAddressChangeEvent((event) => this.emitAddressChange(event));
        this.view.bindTimeChangeEvent((event) => this.emitTimeChange(event));
        this.view.bindSubmitEvent((event) => this.emitSubmit(event));
    }

    emitAddressChange(event){
        this.formEventBus.dispatchEvent(new CustomEvent('FormAddressChange', { detail: event }));
    }
    emitTimeChange(event){
        this.formEventBus.dispatchEvent(new CustomEvent('FormTimeChange', { detail: event }));
    }
    emitSubmit(event){
        event.preventDefault();
        this.formEventBus.dispatchEvent(new CustomEvent('FormSubmit', { detail: event }));
    }
}