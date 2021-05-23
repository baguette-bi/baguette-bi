async function toggleBookmark(id) {
    var res = await fetch(`/api/charts/${id}/bookmark/`, {
        method: 'POST'
    });
    var status = (await res.json()).toggle;

    var element = document.getElementById("bookmark-icon");

    if (status === "added") {
        element.classList.add("bi-bookmark-check-fill");
        element.classList.remove("bi-bookmark");
    } else {
        element.classList.add("bi-bookmark");
        element.classList.remove("bi-bookmark-check-fill");
    }
};
