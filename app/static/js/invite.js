// app/static/js/invite.js
import { showAlert, toggleSpinner } from "./utils.js";

export function initInvite() {
  const form = document.getElementById("invite-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = form.querySelector("button");
    toggleSpinner(btn, true);
    showAlert("");

    const email = document.getElementById("invite-email").value.trim();

    try {
      const res = await fetch("/api/invite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const json = await res.json();

      if (!res.ok) {
        // If detail is an array of validation errors, throw it so catch() can handle
        if (Array.isArray(json.detail)) throw json.detail;
        throw new Error(json.detail || "Failed to send invite");
      }

      showAlert("Invitation sent!", "success");
      form.reset();
    } catch (err) {
      if (Array.isArray(err)) {
        showAlert(err.map((e) => e.msg).join("<br>"));
      } else {
        showAlert(err.message || "Error sending invite");
      }
    } finally {
      toggleSpinner(btn, false);
    }
  });
}

// Immediately wire up the handler
initInvite();
