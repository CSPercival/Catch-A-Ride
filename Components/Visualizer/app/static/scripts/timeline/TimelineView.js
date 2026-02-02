export class TimelineView {
    constructor(){
        this.timelines = {
            car: {
                title : document.getElementById("car-timeline-title"),
                span : document.getElementById("car-timeline-span"),
                body : document.getElementById("car-timeline-body")
            },
            pt: {
                title : document.getElementById("pt-timeline-title"),
                span : document.getElementById("pt-timeline-span"),
                body : document.getElementById("pt-timeline-body")
            },
            duo: {
                title : document.getElementById("duo-timeline-title"),
                span : document.getElementById("duo-timeline-span"),
                body : document.getElementById("duo-timeline-body")
            },
        };
    }

    clearView(){
        Object.keys(this.timelines).forEach(key =>
            this.timelines[key].body.innerHTML = ""
        )
    }

    setTimelineHeights(heightPx){
        Object.keys(this.timelines).forEach(key => {
            this.timelines[key].body.style.height = heightPx + "px";
        });
    }

    setTimelineSpan(key, text){
        if (this.timelines[key].span) this.timelines[key].span.textContent = text ?? "—";
    }
}