import { eventBus } from '../EventBus.js';

export class MapEvents {
    constructor(view){
        this.view = view;

        this.view.bindClickEvent((event) => this.emitMapClick(event));
    }

    emitMapClick(event){
        eventBus.dispatchEvent(new CustomEvent('mapClick', { detail: event.latlng }));
    }
}