function timeToString(time){
    time = ((time % 1440) + 1440) % 1440;
    const hh = String(Math.floor(time/60)).padStart(2,"0");
    const mm = String(time%60).padStart(2,"0");
    return `${hh}:${mm}`;
}

export class TimelineView {
    constructor(){
        this.header = {
            meetingPlace : document.getElementById("meeting-place-span"),
            destinationArrivalSpan : document.getElementById("destination-arrival-span")
        }
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
        Object.keys(this.timelines).forEach(key => {
            this.timelines[key].body.innerHTML = "";
            this.setTimelineSpan(key, "—");
        })
        this.updateMainHeader("—", "—")
    }

    setTimelineHeights(heightPx){
        Object.keys(this.timelines).forEach(key => {
            this.timelines[key].body.style.height = heightPx + "px";
        });
    }

    setTimelineSpan(key, text){
        if (this.timelines[key].span) this.timelines[key].span.textContent = text ?? "—";
    }

    updateMainHeader(meeting_place, arrival_time){
        if(arrival_time !== "—") arrival_time = timeToString(arrival_time)
        console.log("Update timeline main header", meeting_place, arrival_time)
        if(this.header['meetingPlace']) this.header['meetingPlace'].textContent = meeting_place
        if(this.header['destinationArrivalSpan']) this.header['destinationArrivalSpan'].textContent = arrival_time
    }
}