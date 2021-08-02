function getURLParams() {
    const params = new URLSearchParams(document.location.search);
    return Object.fromEntries(params.entries())
}


function getChartParams(el) {
    return JSON.parse(el.dataset.parameters)
}


class ServerException {
    constructor(traceback, status) {
        this.traceback = traceback;
        this.status = status;
    }
}


async function postJSON(url, data) {
    const res = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    });
    const resData = await res.json();
    if (res.status !== 200) {
        throw new ServerException(resData.traceback, res.status);
    }
    return resData
}


function mountFail(el, tb) {
    const container = document.createElement("div");
    container.className = "fail-container d-flex v-100 h-100 align-items-center justify-content-center";
    if (typeof tb === "undefined") {
        const fail = document.createElement("i");
        fail.className = "fail-icon bi-emoji-dizzy";
        container.appendChild(fail);
    } else {
        container.innerText = tb;
    }
    el.replaceChildren(container);
}

async function mountChart(id, el) {
    const parameters = Object.assign(getURLParams(), getChartParams(el));
    try {
        const res = await postJSON(`/api/charts/${id}/render/`, { parameters });
        await vegaEmbed(el, res, { actions: false, ...vegaLocale });
    } catch (err) {
        mountFail(el, err.traceback);
    }
}

function mountAllCharts() {
    const chartDivs = document.querySelectorAll(".pages-chart");
    Promise.all(
        [...chartDivs].map(el => {
            return mountChart(el.dataset.chart, el);
        })
    ).then(() => {
        console.log("all mounted!");
    })
}
