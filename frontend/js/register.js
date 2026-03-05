const BASE = "http://127.0.0.1:9000";

document.addEventListener("DOMContentLoaded", () => {
const form = document.getElementById("registerForm");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const errorMsg = document.getElementById("error");
const btn = document.getElementById("registerBtn");

form.addEventListener("submit", async (e) => {
e.preventDefault();
errorMsg.textContent = "";

if (password.value !== confirmPassword.value) {
  errorMsg.textContent = "Passwords do not match.";
  return;
}

btn.disabled = true;
btn.textContent = "Creating account...";

try {
  const res = await fetch(`${BASE}/api/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: email.value.trim(),
      password: password.value.trim(),
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Registration failed (${res.status})`);
  }

  const data = await res.json();
  alert("Registration successful! Please log in.");
  window.location.href = "login.html";
} catch (err) {
  console.error("Registration error:", err);
  errorMsg.textContent = "Registration failed — " + err.message;
} finally {
  btn.disabled = false;
  btn.textContent = "Register";
}


});
});