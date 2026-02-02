import { TimelineController } from './TimelineController.js';
import { TimelineRenderer } from './TimelineRenderer.js';
import { TimelineState } from './TimelineState.js';
import { TimelineView } from './TimelineView.js';

export class TimelineComponent {
    constructor(){
        this.state = new TimelineState();
        this.view = new TimelineView();
        this.renderer = new TimelineRenderer(this.view);
        this.controller = new TimelineController(this.view, this.state, this.renderer);
    }

    clearTimelines(){
        this.controller.clearTimelines();
    }

    handleOrders(orders){
        this.controller.handleOrders(orders);
    }
}