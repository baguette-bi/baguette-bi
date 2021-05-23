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
    const defn = await postJSON(`/api/charts/${id}/render/`, {});
    const vw = await vegaEmbed("#chart", defn);

    console.log(chart);

    document.getElementById("loader").remove();
    // const init = {
    //     credentials: "same-origin"
    // }
    // const preview = await vw.view.toImageURL("png");
    // await fetch(`/api/charts/${id}/preview/`, Object.assign({
    //     method: "POST",
    //     body: JSON.stringify({ preview }),
    //     headers: {
    //         "Content-Type": "application/json",
    //     },
    // }, init));
}