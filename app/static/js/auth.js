// app/static/js/auth.js

export async function initAuthNavbar() {
  const navAuth = document.getElementById("nav-auth-buttons");
  const navDrop = document.getElementById("nav-user-dropdown");
  const nameSpan = document.getElementById("user-name-display");
  const logoutNav = document.getElementById("logout-nav");

  try {
    const res = await fetch("/api/me");
    if (!res.ok) throw new Error();
    const user = await res.json();

    nameSpan.textContent = user.name;
    navAuth.classList.add("d-none");
    navDrop.classList.remove("d-none");
  } catch {
    navAuth.classList.remove("d-none");
    navDrop.classList.add("d-none");
  }

  logoutNav.addEventListener("click", async (e) => {
    e.preventDefault();
    await fetch("/api/logout");
    window.location.reload();
  });
}
