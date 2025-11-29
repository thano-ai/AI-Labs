function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function runalg() {
    let start = document.getElementById("start").value;
    let goal = document.getElementById("goal").value;

    // Reset colors
    document.querySelectorAll(".city").forEach(c => {
        c.classList.remove("visited", "current", "final-path");
    });

    const response = await fetch("/run_alg", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({start, goal})
    });

    const data = await response.json();
    const steps = data.steps;
    const path = data.path;

    // Animate BFS
    for (let s of steps) {
        let cid = s.current.replace(/ /g, "_");
        let c = document.getElementById(cid);

        if (c) {
            c.classList.add("current");
            await sleep(600);
            c.classList.remove("current");
            c.classList.add("visited");
        }
    }

    // Highlight final path
    if (path) {
        for (let city of path) {
            let cid = city.replace(/ /g, "_");
            let c = document.getElementById(cid);
            if (c) c.classList.add("final-path");
        }
    }

    document.getElementById("output").innerHTML =
        "Final path: " + (path ? path.join(" → ") : "None");
}
