const BASE = window.location.origin;

window.onload = () => {   // 🔥 CHANGE THIS

  const form = document.getElementById("registerForm");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const errorMsg = document.getElementById("error");
  const btn = document.getElementById("registerBtn");

  if (!form) {
    console.error("Form not found ❌");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    console.log("FORM SUBMITTED ✅");

    errorMsg.textContent = "";

    if (password.value !== confirmPassword.value) {
      errorMsg.textContent = "Passwords do not match.";
      return;
    }

    btn.disabled = true;
    btn.textContent = "Creating account...";

    try {
      console.log("Sending request...");

      const res = await fetch(`${BASE}/api/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email.value.trim(),
          password: password.value.trim(),
        }),
      });

      console.log("Response:", res.status);

      if (!res.ok) {
        const text = await res.text();
        console.log("Error:", text);
        throw new Error(text || `Registration failed (${res.status})`);
      }

      alert("Registration successful!");
      window.location.href = "login.html";

    } catch (err) {
      console.error("Registration error:", err);
      errorMsg.textContent = "Registration failed — " + err.message;
    } finally {
      btn.disabled = false;
      btn.textContent = "Register";
    }
  });
};