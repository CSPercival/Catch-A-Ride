import { FormView } from './FormView.js';
import { FormEvents } from './FormEvents.js';
import { FormState } from './FormState.js';
import { FormController } from './FormController.js';
import { formEventBus } from './FormEventBus.js'
import { mainEventBus } from './../EventBus.js'

export class FormComponent {
    constructor(){
        this.view = new FormView();
        this.state = new FormState();
        this.events = new FormEvents(this.view, formEventBus);
        this.controller = new FormController(this.view, this.state, mainEventBus, formEventBus);
    }

    updateInvalidAddress(new_place){
        this.controller.updateInvalidAddress(new_place);
    }
}