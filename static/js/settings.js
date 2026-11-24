/* ---------- Settings: theme, bubble color, delete modal ---------- */
const THEME_KEY = "pp_theme";
const BUBBLE_KEY = "pp_bubble";
const BUBBLE_COLORS = {
  orange: "#FF5A36",
  purple: "#7C3AED",
  cyan: "#06B6D4",
  green: "#10B981",
  pink: "#EC4899",
};
const DELETE_WORD = "DELETE";
const systemDark = window.matchMedia("(prefers-color-scheme: dark)");

function resolveTheme(mode) {
  if (mode === "system") return systemDark.matches ? "dark" : "light";
  return mode;
}

function applyTheme(mode) {
  document.documentElement.classList.toggle(
    "dark",
    resolveTheme(mode) === "dark",
  );
  document.querySelectorAll("[data-theme-option]").forEach((btn) => {
    const on = btn.dataset.themeOption === mode;
    btn.classList.toggle("is-selected", on);
    btn.setAttribute("aria-checked", on);
  });
}

function setAppTheme(mode) {
  localStorage.setItem(THEME_KEY, mode);
  applyTheme(mode);
}

function applyBubbleColor(key) {
  const hex = BUBBLE_COLORS[key] || BUBBLE_COLORS.orange;
  document.documentElement.style.setProperty("--bubble-own", hex);
  document.querySelectorAll("[data-bubble]").forEach((btn) => {
    const on = btn.dataset.bubble === key;
    btn.classList.toggle("is-selected", on);
    btn.setAttribute("aria-checked", on);
  });
}

function setBubbleColor(key) {
  localStorage.setItem(BUBBLE_KEY, key);
  applyBubbleColor(key);
}


(function applyStoredPrefs() {
  const mode = localStorage.getItem(THEME_KEY) || "dark";
  document.documentElement.classList.toggle(
    "dark",
    resolveTheme(mode) === "dark",
  );
  document.documentElement.style.setProperty(
    "--bubble-own",
    BUBBLE_COLORS[localStorage.getItem(BUBBLE_KEY)] || BUBBLE_COLORS.orange,
  );
})();


systemDark.addEventListener("change", () => {
  if (localStorage.getItem(THEME_KEY) === "system") applyTheme("system");
});


document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("[data-theme-option]")) {
    applyTheme(localStorage.getItem(THEME_KEY) || "dark");
  }
  if (document.querySelector("[data-bubble]")) {
    applyBubbleColor(localStorage.getItem(BUBBLE_KEY) || "orange");
  }
});

