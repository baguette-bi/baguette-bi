function getURLParams() {
    const params = new URLSearchParams(document.location.search);
    return Object.fromEntries(params.entries())
}


function getChartParams(el) {
    return JSON.parse(el.dataset.parameters)
}


async function postJSON(url, data) {
    try {
        const res = await fetch(url, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (res.status !== 200) {
            return null
        }
        return res.json()
    } catch {
        return null
    }
}


function mountFail(el) {
    const container = document.createElement("div");
    container.className = "fail-container d-flex v-100 h-100 align-items-center justify-content-center";
    const fail = document.createElement("i");
    fail.className = "fail-icon bi-emoji-dizzy";
    container.appendChild(fail);
    el.replaceChildren(container);
}

async function mountChart(id, el) {
    const parameters = Object.assign(getURLParams(), getChartParams(el));
    const res = await postJSON(`/api/charts/${id}/render/`, { parameters });
    if (res === null) {
        mountFail(el);
        return
    }
    await vegaEmbed(el, res, { actions: false, ...vegaLocale });
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
