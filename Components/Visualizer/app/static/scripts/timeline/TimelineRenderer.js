// TimelineRenderer.js
export class TimelineRenderer {
  constructor(view, { pxPerMin = 8, minBlockHeight = 78, minGap = 10 } = {}) {
    this.view = view;
    this.pxPerMin = pxPerMin;
    this.minBlockHeight = minBlockHeight;
    this.minGap = minGap;
    this.topPadding = 12; // musi pasować do paddingu w CSS TimelineBody
  }

  setScale(pxPerMin) {
    this.pxPerMin = pxPerMin;
    document.documentElement.style.setProperty("--pxPerMin", pxPerMin + "px");
  }

  renderAll(appState) {
    // appState = state.getState()
    const { timelines, startTime, finishTime } = appState;

    // const totalMin = Math.max(1, finishTime - startTime);
    // const heightPx = Math.ceil(totalMin * this.pxPerMin) + this.topPadding * 2;

    this.view.setTimelineSpan("car", this.computeSpan(timelines.car.line));
    this.view.setTimelineSpan("pt", this.computeSpan(timelines.pt.line));
    this.view.setTimelineSpan("duo", this.computeSpan(timelines.duo.line));

    this.renderTimeline(this.view.timelines.car.body, timelines.car.line, startTime, "car");
    this.renderTimeline(this.view.timelines.pt.body, timelines.pt.line, startTime, "pt");
    this.renderTimeline(this.view.timelines.duo.body, timelines.duo.line, startTime, "duo");
  }

  computeSpan(line) {
    if (!line || line.length === 0) return "—";
    const first = line[0];
    const last = line[line.length - 1];
    return `${first.startTimeString} → ${last.finishTimeString}`;
  }

  renderTimeline(container, line, globalStartTime, kind) {
    // line powinno być posortowane po startTimeNumber
    // let lastBottom = -Infinity;

    // for (const seg of line) {
    //   const startMin = seg.startTimeNumber - globalStartTime;
    //   const durMin = Math.max(1, seg.finishTimeNumber - seg.startTimeNumber);

    //   let top = Math.round(startMin * this.pxPerMin) + this.topPadding;
    //   let height = Math.max(this.minBlockHeight, Math.round(durMin * this.pxPerMin));

    //   // prosta antykolizja (czytelność)
    //   if (top < lastBottom + this.minGap) top = lastBottom + this.minGap;
    //   lastBottom = top + height;

    //   const node = document.createElement("article");
    //   node.className = `range ${kind} minH`;
    //   node.style.top = top + "px";
    //   node.style.height = height + "px";

    //   const timeText = `${seg.startTimeString} → ${seg.finishTimeString} • ${seg.durationString}`;
    container.innerHTML = ''; 

    for (const seg of line) {
      
      const node = document.createElement("article");
      node.className = `range relative-block ${kind}`; 
      
      const timeText = `${seg.startTimeString} → ${seg.finishTimeString} • ${seg.durationString}`;

      node.innerHTML = `
        <div class="rangeHeader">
          <h3 class="rangeTitle">${this.escapeHtml(seg.title ?? "")}</h3>
          <div class="rangeTime">${this.escapeHtml(timeText)}</div>
        </div>

        <details class="desc">
          <summary>Description</summary>
          <div class="descBody">${this.renderDescription(seg.description)}</div>
        </details>
      `;

      container.appendChild(node);
    }
  }

  renderDescription(description) {
    if (!description) return `<em style="color:rgba(238,242,255,.65)">Brak opisu.</em>`;

    if (typeof description === "string") {
      return `<div>${this.escapeHtml(description)}</div>`;
    }

    if (Array.isArray(description)) {
      return `<ul>${description.map(x => `<li>${this.escapeHtml(x)}</li>`).join("")}</ul>`;
    }

    if (typeof description === "object") {
      const text = description.text ? `<div>${this.escapeHtml(description.text)}</div>` : "";
      const stops = Array.isArray(description.stops)
        ? `<ul>${description.stops.map(s => `<li>${this.escapeHtml(s)}</li>`).join("")}</ul>`
        : "";
      return text + stops;
    }

    return `<div>${this.escapeHtml(String(description))}</div>`;
  }

  escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
}
