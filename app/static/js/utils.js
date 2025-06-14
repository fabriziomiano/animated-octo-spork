// app/static/js/utils.js
export function toggleSpinner(btn, show) {
  const spinner = btn.querySelector(".spinner-border");
  const textEl = btn.querySelector(".btn-text");
  const original = btn.dataset.originalText;
  if (show) {
    spinner.classList.remove("d-none");
    textEl.textContent = "Please wait...";
  } else {
    spinner.classList.add("d-none");
    textEl.textContent = original;
  }
}

export function showAlert(msg, type = "danger") {
  const container = document.getElementById("alert-container");
  if (!container) return; // bail out silently
  container.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`;
}
