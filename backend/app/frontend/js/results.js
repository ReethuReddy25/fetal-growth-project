console.log("RESULTS JS LOADED");

document.addEventListener("DOMContentLoaded", () => {

  const data = JSON.parse(localStorage.getItem("latestResult"));

  const container = document.getElementById("resultsContainer");
  const noResult = document.getElementById("noResult");

  // ❌ No data case
  if (!data) {
    if (noResult) noResult.style.display = "block";
    return;
  }

  // ✅ Hide "No result"
  if (noResult) noResult.style.display = "none";

  // 🎨 Status color
  let statusColor = "#999";

  if (data.growth_status === "AGA") {
    statusColor = "#28a745"; // green
  } else if (data.growth_status === "SGA") {
    statusColor = "#dc3545"; // red
  } else {
    statusColor = "#ffc107"; // orange
  }

  // ✅ Render UI
  container.innerHTML = `
    <div class="card" style="max-width:500px;margin:auto;text-align:left;">

      <h2 style="text-align:center;">Prediction Result</h2>

      <div style="text-align:center; margin:20px 0;">
        <span style="
          background:${statusColor};
          color:white;
          padding:10px 20px;
          border-radius:25px;
          font-weight:bold;
          font-size:16px;
        ">
          ${data.growth_status}
        </span>
      </div>

      <p><strong>Average Head Circumference:</strong> ${data.average_head_circumference_mm} mm</p>

      <p><strong>Z-Score:</strong> ${data.z_score}</p>

      <p><strong>Scale Factor:</strong> ${data.applied_scale_factor}</p>

      <p><strong>Head Circumference per image (mm):</strong></p>

      <ul style="padding-left:20px;">
        ${data.predictions_per_image.map(val => `<li>${val}</li>`).join("")}
      </ul>

    </div>
  `;
});