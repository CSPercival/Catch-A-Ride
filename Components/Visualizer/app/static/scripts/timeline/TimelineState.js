function timeToString(time){
    time = ((time % 1440) + 1440) % 1440;
    const hh = String(Math.floor(time/60)).padStart(2,"0");
    const mm = String(time%60).padStart(2,"0");
    return `${hh}:${mm}`;
}
function durationToString(time){
    let ans = ""
    if(time >= 60){
        ans = ans + String(Math.floor(time/60)) + "h ";
    }
    ans = ans + String(time%60).padStart(2, '0') + "min";
    return ans;
}

export class TimelineState {
    constructor(){
        this.timelines = {
            car: {
                header: {},
                line: []
            },
            pt: {
                header: {},
                line: []
            },
            duo: {
                header: {},
                line: []
            }
        };
        this.meetingPlace = null;
        this.startTime = Infinity;
        this.meetingTime = -Infinity;
        this.finishTime = -Infinity;
    }

    clearState(){
        this.timelines = {
            car: {
                header: {},
                line: []
            },
            pt: {
                header: {},
                line: []
            },
            duo: {
                header: {},
                line: []
            }
        };
        this.meetingPlace = null;
        this.startTime = Infinity;
        this.meetingTime = -Infinity;
        this.finishTime = -Infinity;
    }

    getState(){
        return {
            timelines: this.timelines,
            meetingPlace: this.meetingPlace,
            startTime: this.startTime,
            meetingTime: this.meetingTime,
            finishTime: this.finishTime
        };
    }

    createSegment(title, description, startTime, finishTime, duration){
        return {
            title: title,
            description: description,
            startTimeNumber: startTime,
            startTimeString: timeToString(startTime),
            finishTimeNumber: finishTime,
            finishTimeString: timeToString(finishTime),
            durationNumber: duration,
            durationString: durationToString(duration)
        };
    }

    updateMainHeader(meetingPlace, duration){
        this.meetingPlace = meetingPlace;
        this.duration = duration;
    }

    updateTimelineHeader(key, startLocation, finishLocation){
        this.timelines[key].header = {
            startLocation: startLocation,
            finishLocation: finishLocation,
        };
    }

    addSegment(key, title, description, startTime, finishTime, duration){
        const newSegment = this.createSegment(title, description, startTime, finishTime, duration);
        if(this.timelines[key].line.length > 0 && this.timelines[key].line.at(-1).finishTimeNumber > startTime){
            console.log("ERROR, timeline not sorted");
            console.log(key, this.timelines[key].line, newSegment);
            return;
        }
        this.startTime = Math.min(this.startTime, startTime);
        this.finishTime = Math.max(this.finishTime, finishTime);
        this.timelines[key].line.push(newSegment);
        if(key !== "duo"){
            this.meetingTime = Math.max(this.meetingTime, finishTime);
        }
    }
}