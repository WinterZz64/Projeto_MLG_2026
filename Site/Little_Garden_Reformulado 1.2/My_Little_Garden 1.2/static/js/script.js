document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    });
  }

  document.querySelectorAll(".detail-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const details = button.nextElementSibling;
      const isOpen = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!isOpen));
      details.hidden = isOpen;
      const symbol = button.querySelector("span");
      if (symbol) symbol.textContent = isOpen ? "＋" : "−";
    });
  });

  const password = document.querySelector("#password");
  const confirmation = document.querySelector("#confirm_password");
  if (password && confirmation) {
    const checkMatch = () => {
      confirmation.setCustomValidity(
        confirmation.value && confirmation.value !== password.value
          ? "As senhas não coincidem."
          : ""
      );
    };
    password.addEventListener("input", checkMatch);
    confirmation.addEventListener("input", checkMatch);
  }
});
