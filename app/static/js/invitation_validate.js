document.addEventListener("DOMContentLoaded", async () => {
  const statusEl = document.getElementById("status-message");
  const code = new URLSearchParams(window.location.search).get("code");
  if (!code) {
    statusEl.innerHTML = `<div class="text-danger">No code provided</div>`;
    return;
  }

  try {
    const res = await fetch(
      `/api/invitation/validate?code=${encodeURIComponent(code)}`
    );
    const { valid } = await res.json();
    if (valid) {
      statusEl.innerHTML = `<div class="text-success">Invite is valid! You can now register.</div>`;
    } else {
      statusEl.innerHTML = `<div class="text-danger">Invalid or used code.</div>`;
    }
  } catch {
    statusEl.innerHTML = `<div class="text-danger">Error checking code.</div>`;
  }
});
