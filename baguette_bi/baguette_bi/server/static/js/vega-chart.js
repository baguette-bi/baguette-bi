function getParams() {
    const params = new URLSearchParams(document.location.search);
    return Object.fromEntries(params.entries())
}


async function postJSON(url, data) {
    const res = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    return res.json()
}


async function mountChart(id, el) {
    const res = await postJSON(`/api/charts/${id}/render/`, { parameters: getParams() });
    if (typeof(res.traceback) !== "undefined") {
        console.log(res.traceback);
        alert("Error loading chart, please contact server administrator.");
    } else {
        await vegaEmbed(el, res, { actions: false });
    }
    const loader = document.getElementById("loader");
    if (loader !== null) {
        loader.remove();
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