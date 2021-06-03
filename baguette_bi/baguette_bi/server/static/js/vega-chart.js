const fetchData = (chartId, vegaView) => async([id, dataset]) => {
    console.log(dataset);
    const res = await fetch(`/api/charts/${chartId}/datasets/${id}/data/`, { method: "POST" })
    const values = await res.json()
    console.log(values);
    vegaView.insert(id, values);
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


async function mountChart(id) {
    const res = await postJSON(`/api/charts/${id}/render/`, {});
    if (typeof(res.traceback) !== "undefined") {
        console.log(res.traceback);
        alert("Error loading chart, please contact server administrator.");
    } else {
        const vw = await vegaEmbed("#chart", res);
    }
    document.getElementById("loader").remove();
}