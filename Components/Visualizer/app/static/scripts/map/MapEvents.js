// import { eventBus } from '../EventBus.js';

export class MapEvents {
    constructor(view, mainEventBus){
        this.view = view;
        this.mainEventBus = mainEventBus;

        this.view.bindClickEvent((event) => this.emitMapClick(event));
    }

    emitMapClick(event){
        this.mainEventBus.dispatchEvent(new CustomEvent('mapClick', { detail: event.latlng }));
    }
}