document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");

  if (toggle && nav) {
    const closeMenu = () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Abrir menu");
    };

    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
        toggle.focus();
      }
    });

    document.addEventListener("click", (event) => {
      if (
        nav.classList.contains("open") &&
        !nav.contains(event.target) &&
        !toggle.contains(event.target)
      ) {
        closeMenu();
      }
    });
  }

  document.querySelectorAll(".detail-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const details = button.nextElementSibling;
      if (!details) return;
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
