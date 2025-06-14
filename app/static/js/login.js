// app/static/js/login.js
import { showAlert, toggleSpinner } from "./utils.js";

export function initLogin() {
  const loginForm = document.getElementById("login-form");
  const twoFaForm = document.getElementById("2fa-form");
  if (!loginForm) return;

  // ——— Login (email+password) ——————————————————————————————
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = loginForm.querySelector("button");
    toggleSpinner(btn, true);
    showAlert("");

    const payload = new URLSearchParams();
    payload.append(
      "username",
      document.getElementById("login-email").value.trim()
    );
    payload.append("password", document.getElementById("login-password").value);

    try {
      const res = await fetch("/api/login", { method: "POST", body: payload });
      const json = await res.json();

      if (!res.ok) {
        // If detail is an array of Pydantic errors, throw it
        if (Array.isArray(json.detail)) throw json.detail;
        throw new Error(json.detail || "Login failed");
      }

      if (json.twofa_required) {
        showAlert(
          `2FA code sent. (DEV code: <strong>${json.twofa_code}</strong>)`,
          "info"
        );
        loginForm.classList.add("d-none");
        twoFaForm.classList.remove("d-none");
      } else {
        showAlert("Logged in!", "success");
        setTimeout(() => (window.location.href = "/invite"), 500);
      }
    } catch (err) {
      if (Array.isArray(err)) {
        showAlert(err.map((e) => e.msg).join("<br>"));
      } else {
        showAlert(err.message || "Error logging in");
      }
    } finally {
      toggleSpinner(btn, false);
    }
  });

  // ——— 2FA verification —————————————————————————————————
  twoFaForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = twoFaForm.querySelector("button");
    toggleSpinner(btn, true);
    showAlert("");

    const email = document.getElementById("login-email").value.trim();
    const code = document.getElementById("2fa-code").value.trim();

    try {
      const res = await fetch("/api/login/2fa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code }),
      });
      const json = await res.json();

      if (!res.ok) {
        if (Array.isArray(json.detail)) throw json.detail;
        throw new Error(json.detail || "Invalid 2FA code");
      }

      showAlert("Logged in successfully!", "success");
      setTimeout(() => (window.location.href = "/invite"), 500);
    } catch (err) {
      if (Array.isArray(err)) {
        showAlert(err.map((e) => e.msg).join("<br>"));
      } else {
        showAlert(err.message || "2FA verification failed");
      }
    } finally {
      toggleSpinner(btn, false);
    }
  });
}

// Immediately wire up the handler
initLogin();
