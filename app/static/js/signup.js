// app/static/js/signup.js
import { showAlert, toggleSpinner } from "./utils.js";

// Debug: confirm the module loaded
console.log("signup.js loaded");

export function initSignup() {
  console.log("initSignup() running");
  const form = document.getElementById("signup-form");
  if (!form) {
    console.warn("no #signup-form found");
    return;
  }

  // Capture invitation code from query string if present
  const params = new URLSearchParams(window.location.search);
  const invitationCode = params.get("code");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("signup form submit");

    const btn = form.querySelector("button");
    toggleSpinner(btn, true);
    showAlert(""); // clear

    const data = {
      name: document.getElementById("signup-name").value.trim(),
      email: document.getElementById("signup-email").value.trim(),
      password: document.getElementById("signup-password").value,
    };

    // If we came from an invitation link, include the code
    if (invitationCode) {
      data.invitation_code = invitationCode;
    }

    try {
      const res = await fetch("/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      console.log("Signup response:", res.status, json);

      if (!res.ok) {
        if (Array.isArray(json.detail)) throw json.detail;
        throw new Error(json.detail || "Signup failed");
      }

      showAlert("Signup successful! Redirecting…", "success");
      form.reset();
      setTimeout(() => (window.location.href = "/invite"), 500);
    } catch (err) {
      console.error("Signup error:", err);
      if (Array.isArray(err)) {
        showAlert(err.map((e) => e.msg).join("<br>"));
      } else {
        showAlert(err.message || "Error signing up");
      }
    } finally {
      toggleSpinner(btn, false);
    }
  });
}

// Immediately wire up the handler
initSignup();
