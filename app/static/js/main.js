// app/static/js/main.js
import { initAuthNavbar } from "./auth.js";
import { initInvite } from "./invite.js";
import { initLogin } from "./login.js";
import { initSignup } from "./signup.js";

document.addEventListener("DOMContentLoaded", () => {
  initAuthNavbar();
  initSignup();
  initLogin();
  initInvite();
});
