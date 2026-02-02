export class TimelineController {
    constructor(view, state, renderer){
        this.view = view;
        this.state = state;
        this.renderer = renderer;
    }
    
    handleOrders(orders){
        this.state.updateMainHeader(orders['header']['meetingPointName'], orders['header']['journeyDuration']);
        const keys = ['car','pt','duo'];
        keys.forEach(key => {
            orders[key].events.forEach(event => {
                console.log(key, event);
                this.state.addSegment(key, event.title, event.description, event.startTime, event.finishTime, event.duration);
            });
        });
        console.log(this.state.getState());

        this.renderer.renderAll(this.state.getState());
    }

    clearTimelines(){
        this.state.clearState();
        this.view.clearView();
    }
}