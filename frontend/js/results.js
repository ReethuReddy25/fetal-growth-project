// js/results.js

document.addEventListener("DOMContentLoaded", () => {

  // check if user logged in
  if (typeof requireAuth === "function") {
    requireAuth();
  }

  const container = document.getElementById("resultsContainer");
  const noResult = document.getElementById("noResult");

  if (!container || !noResult) {
    console.error("Required result elements not found in HTML.");
    return;
  }

  // get saved prediction from upload step
  const raw = localStorage.getItem("latestResult");

  if (!raw) {
    noResult.style.display = "block";
    return;
  }

  let data;

  try {
    data = JSON.parse(raw);
  } catch (err) {
    console.error("Result parse error:", err);
    noResult.style.display = "block";
    noResult.querySelector("p").textContent =
      "Stored result is corrupted. Please run detection again.";
    return;
  }

  // hide no-result message
  noResult.style.display = "none";
  container.innerHTML = "";

  /* =========================
     RESULT CARD
  ========================== */

  const card = document.createElement("div");
  card.className = "result-card";

  const main = document.createElement("div");
  main.style.flex = "1";

  /* Growth Status */
  const tag = document.createElement("div");
  tag.className = "tag " + (data.growth_status || "unknown").toLowerCase();
  tag.textContent = data.growth_status || "Unknown";
  main.appendChild(tag);

  /* Main Metrics */
  const details = document.createElement("div");
  details.className = "muted small";
  details.style.marginTop = "10px";

  const avg = data.average_head_circumference_mm ?? "N/A";
  const z = data.z_score ?? "N/A";
  const scale = data.applied_scale_factor ?? "N/A";

  details.innerHTML = `
    <b>Average Head Circumference:</b>
    ${typeof avg === "number" ? avg.toFixed(2) : avg} mm<br><br>

    <b>Z-Score:</b> ${typeof z === "number" ? z.toFixed(3) : z}<br>
    <b>Scale Factor:</b> ${typeof scale === "number" ? scale.toFixed(3) : scale}
  `;

  main.appendChild(details);

  /* Per Image Predictions */
  if (Array.isArray(data.predictions_per_image)) {

    const perImg = document.createElement("pre");
    perImg.className = "small-pre";

    const values = data.predictions_per_image
      .map(v => (typeof v === "number" ? v.toFixed(2) : v))
      .join(", ");

    perImg.textContent =
      "Head Circumference per image (mm):\n" + values;

    main.appendChild(perImg);
  }

  /* Append card */
  card.appendChild(main);
  container.appendChild(card);

});