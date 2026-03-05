// js/results.js
document.addEventListener("DOMContentLoaded", () => {
  requireAuth();

  const container = document.getElementById("resultsContainer");
  const noResult = document.getElementById("noResult");

  // 🔹 Correct key used in upload.js
  const raw = localStorage.getItem("latestResult");

  if (!raw) {
    noResult.style.display = "block";
    return;
  }

  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    noResult.style.display = "block";
    noResult.querySelector("p").textContent =
      "Stored result is corrupted. Please run detection again.";
    return;
  }

  // Hide "no result" message
  noResult.style.display = "none";
  container.innerHTML = "";

  /* ===============================
     MAP BACKEND RESPONSE
  ================================ */

  const card = document.createElement("div");
  card.className = "result-card";

  const main = document.createElement("div");
  main.style.flex = "1";

  // 🔹 Growth status (SGA / AGA / LGA)
  const tag = document.createElement("div");
  tag.className = "tag " + data.growth_status.toLowerCase();
  tag.textContent = data.growth_status;
  main.appendChild(tag);

  // 🔹 Main metrics
  const details = document.createElement("div");
  details.className = "muted small";
  details.style.marginTop = "10px";
  details.innerHTML = `
    <b>Average Head Circumference:</b>
    ${data.average_head_circumference_mm.toFixed(2)} mm<br><br>

    <b>Z-Score:</b> ${data.z_score.toFixed(3)}<br>
    <b>Scale Factor:</b> ${data.applied_scale_factor.toFixed(3)}
  `;
  main.appendChild(details);

  // 🔹 Per-image predictions
  if (Array.isArray(data.predictions_per_image)) {
    const perImg = document.createElement("pre");
    perImg.className = "small-pre";
    perImg.textContent =
      "Head Circumference per image (mm):\n" +
      data.predictions_per_image.map(v => v.toFixed(2)).join(", ");
    main.appendChild(perImg);
  }

  card.appendChild(main);
  container.appendChild(card);
});
