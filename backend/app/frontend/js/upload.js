/* ===============================
   upload.js – DEPLOYMENT VERSION
================================ */

const BASE = window.location.origin;

const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");
const gallery = document.getElementById("gallery");
const runBtn = document.getElementById("runBtn");
const resetBtn = document.getElementById("resetBtn");
const logoutBtn = document.getElementById("logoutBtn");

let selectedFiles = [];

/* ===============================
   OPEN FILE PICKER
================================ */
dropArea.addEventListener("click", () => {
  fileInput.click();
});

/* ===============================
   FILE SELECTION
================================ */
fileInput.addEventListener("change", (e) => {
  selectedFiles = Array.from(e.target.files);
  showPreviews();
});

/* ===============================
   DRAG & DROP
================================ */
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.classList.add("drag-over");
});

dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("drag-over");
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.classList.remove("drag-over");

  selectedFiles = Array.from(e.dataTransfer.files);
  showPreviews();
});

/* ===============================
   IMAGE PREVIEW
================================ */
function showPreviews() {
  gallery.innerHTML = "";

  selectedFiles.forEach((file) => {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.className = "thumb";
    gallery.appendChild(img);
  });
}

/* ===============================
   RUN DETECTION
================================ */
runBtn.addEventListener("click", async () => {

  const gaWeeks = document.getElementById("gaWeeks").value;

  if (!gaWeeks) {
    alert("Please enter gestational age in weeks.");
    return;
  }

  if (selectedFiles.length === 0) {
    alert("Please select at least one image.");
    return;
  }

  const token = localStorage.getItem("fg_token");

  if (!token) {
    alert("Session expired. Please login again.");
    window.location.href = "/login";   // ✅ FIXED
    return;
  }

  const formData = new FormData();

  formData.append("gestational_age", parseInt(gaWeeks));

  selectedFiles.forEach((file) => {
    formData.append("files", file);
  });

  try {

    const response = await fetch(`${BASE}/api/predict/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error("Prediction failed");
    }

    const result = await response.json();

    localStorage.setItem("latestResult", JSON.stringify(result));

    alert("Detection completed successfully!");

    window.location.href = "/results";   // ✅ FIXED

  } catch (error) {
    console.error("Error during detection:", error);
    alert("Prediction failed. Please try again.");
  }

});

/* ===============================
   RESET
================================ */
resetBtn.addEventListener("click", () => {
  selectedFiles = [];
  gallery.innerHTML = "";
  fileInput.value = "";
  document.getElementById("gaWeeks").value = "";
});

/* ===============================
   LOGOUT
================================ */
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("fg_token");
  window.location.href = "/login";   // ✅ FIXED
});