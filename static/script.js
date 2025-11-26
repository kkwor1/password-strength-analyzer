document.getElementById("password").addEventListener("input", async function () {
    const password = this.value;

    // Clear UI for empty input
    if (password.length === 0) {
        resetUI();
        return;
    }

    // Send to backend
    const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
    });

    const data = await response.json();

    updateUI(data);
});

// Reset UI when empty
function resetUI() {
    document.getElementById("strength-bar").style.width = "0%";
    document.getElementById("strength-text").textContent = "Start typing to analyze...";
    document.getElementById("len").textContent = "—";
    document.getElementById("charset").textContent = "—";
    document.getElementById("comb").textContent = "—";
    document.getElementById("entropy").textContent = "—";
    document.getElementById("time").textContent = "—";
}

// Update UI with API data
function updateUI(data) {
    const bar = document.getElementById("strength-bar");
    const text = document.getElementById("strength-text");

    // Set bar width + color depending on strength
    let width = 0;
    let color = "#ff4d4d"; // default red

    switch (data.strength) {
        case "Weak":
            width = 20;
            color = "#ff4d4d";
            break;
        case "Moderate":
            width = 45;
            color = "#ffa534";
            break;
        case "Strong":
            width = 70;
            color = "#4caf50";
            break;
        case "Very Strong":
            width = 100;
            color = "#006400";
            break;
    }

    bar.style.width = width + "%";
    bar.style.backgroundColor = color;

    // Text feedback
    text.textContent = data.strength + " — " + (data.feedback || "");

    // Numerical values
    document.getElementById("len").textContent = data.length;
    document.getElementById("charset").textContent = data.charset;
    document.getElementById("comb").textContent = data.combinations;
    document.getElementById("entropy").textContent = data.entropy.toFixed(2) + " bits";
    document.getElementById("time").textContent = data.time_1e9;
}

// --------------------
// Toggle show/hide password
// --------------------
(function () {
    const toggle = document.getElementById("toggle-eye");
    const pwd = document.getElementById("password");
    if (!toggle || !pwd) return;

    toggle.addEventListener("click", function () {
        const isHidden = pwd.type === "password";
        pwd.type = isHidden ? "text" : "password";
        toggle.classList.toggle("visible", isHidden);
        // update aria-label
        toggle.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
    });
})();
