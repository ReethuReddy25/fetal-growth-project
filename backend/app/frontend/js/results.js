console.log("RESULTS JS LOADED");

document.addEventListener("DOMContentLoaded", () => {

  const data = JSON.parse(localStorage.getItem("latestResult"));

  if (!data) {
    alert("No results found");
    window.location.href = "/upload";   // ✅ FIXED
    return;
  }

  const output = document.getElementById("resultsContainer");  // ✅ FIXED

  output.innerHTML = `
    <h2>Prediction Result</h2>
    <pre>${JSON.stringify(data, null, 2)}</pre>
  `;

});