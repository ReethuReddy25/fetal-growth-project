const BASE = "https://fetal-growth-api.onrender.com";

function saveToken(token) {
localStorage.setItem("fg_token", token);
}

function getToken() {
return localStorage.getItem("fg_token");
}

function clearToken() {
localStorage.removeItem("fg_token");
}

function requireAuth() {
if (!getToken()) window.location.href = "login.html";
}

function goToUploadIfAuth() {
if (getToken()) window.location.href = "upload.html";
}

document.addEventListener("DOMContentLoaded", () => {

if (document.getElementById("loginForm")) {

const form = document.getElementById("loginForm");
const email = document.getElementById("email");
const password = document.getElementById("password");
const err = document.getElementById("error");
const demo = document.getElementById("demoBtn");

demo?.addEventListener("click", () => {
  email.value = "doctor@example.com";
  password.value = "password";
});

form.addEventListener("submit", async (e) => {

  e.preventDefault();
  err.textContent = "";

  const submitBtn = document.getElementById("submitBtn");
  submitBtn.disabled = true;
  submitBtn.textContent = "Signing in...";

  try {

    const res = await fetch(`${BASE}/api/users/login`, {
      method: "POST",
      body: new URLSearchParams({
        username: email.value,
        password: password.value,
      }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Login failed (${res.status})`);
    }

    const data = await res.json();

    if (!data.access_token && !data.token) {
      throw new Error("No token returned by server");
    }

    saveToken(data.access_token || data.token);

    alert("Login successful!");
    window.location.href = "upload.html";

  } catch (error) {

    console.error("Login error:", error);
    err.textContent = "Login failed — " + error.message;

  } finally {

    submitBtn.disabled = false;
    submitBtn.textContent = "Sign in";

  }

});

}

const logoutBtns = document.querySelectorAll("#logout, #logoutBtn");

logoutBtns.forEach((btn) =>
btn.addEventListener("click", () => {
clearToken();
window.location.href = "login.html";
})
);

const goResults = document.getElementById("goResults");
if (goResults) goResults.addEventListener("click", () => window.location.href = "results.html");

const goUpload = document.getElementById("goUpload");
if (goUpload) goUpload.addEventListener("click", () => window.location.href = "upload.html");

const goLogin = document.getElementById("goLogin");
if (goLogin) goLogin.addEventListener("click", () => window.location.href = "login.html");

});