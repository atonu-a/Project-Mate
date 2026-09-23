/* ---------- Theme ---------- */
function toggleTheme() {
  const html = document.documentElement;
  if (html.classList.contains("dark")) {
    html.classList.remove("dark");
    localStorage.setItem("pp_theme", "light");
  } else {
    html.classList.add("dark");
    localStorage.setItem("pp_theme", "dark");
  }
}

// Apply the stored theme on load
(function () {
  const savedTheme = localStorage.getItem("pp_theme");
  if (savedTheme === "light") {
    document.documentElement.classList.remove("dark");
  } else {
    document.documentElement.classList.add("dark");
  }
})();

/* ---------- Menus ---------- */
function toggleUserMenu() {
  const menu = document.getElementById("userDropdown");
  if (menu) menu.classList.toggle("is-open");
}

// Close the user dropdown when tapping anywhere outside it
document.addEventListener("click", (event) => {
  const menu = document.getElementById("userDropdown");
  if (menu && !event.target.closest(".user-menu")) {
    menu.classList.remove("is-open");
  }
});

function toggleMobileMenu() {
  const menu = document.getElementById("mobileMenu");
  if (!menu) return;
  menu.classList.toggle("is-open");
  // Stop the page behind the drawer from scrolling
  document.body.classList.toggle(
    "menu-open",
    menu.classList.contains("is-open"),
  );
}

/* ---------- Toasts ---------- */
function showToast(message, type = "success") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const isSuccess = type === "success";
  const toast = document.createElement("div");
  toast.className = `toast ${isSuccess ? "toast--success" : "toast--info"}`;

  const icon = document.createElement("i");
  icon.setAttribute(
    "data-lucide",
    isSuccess ? "check-circle-2" : "alert-circle",
  );
  icon.className = "toast__icon";

  const text = document.createElement("span");
  text.className = "toast__message";
  text.textContent = message;

  toast.append(icon, text);
  container.appendChild(toast);
  if (typeof lucide !== "undefined") lucide.createIcons();

  setTimeout(() => toast.classList.add("is-visible"), 10);

  setTimeout(() => {
    toast.classList.remove("is-visible");
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/* ---------- Feed actions ---------- */
function toggleLike(btn) {
  const label = btn.querySelector("span");
  const count = parseInt(label.textContent, 10) || 0;

  if (btn.classList.contains("is-liked")) {
    btn.classList.remove("is-liked");
    label.textContent = `${count - 1} Likes`;
  } else {
    btn.classList.add("is-liked");
    label.textContent = `${count + 1} Likes`;
    showToast("Project bookmarked & liked!");
  }
}

function toggleComments(btn) {
  showToast("Comments panel opened", "info");
}

/* ---------- Join requests ---------- */
// Called from the Accept / Reject buttons on requests.html
function respondToRequest(btn, decision) {
  const card = btn.closest(".request");
  const actions = btn.closest(".request__actions");
  const applicant = card && card.dataset.applicant;
  const accepted = decision === "accept";

  if (accepted) {
    showToast(
      applicant
        ? `Accepted join request from ${applicant}!`
        : "Accepted join request!",
    );
  } else {
    showToast("Declined request", "info");
  }

  if (actions) {
    actions.innerHTML = accepted
      ? '<span class="status-pill">Accepted</span>'
      : '<span class="status-pill status-pill--declined">Declined</span>';
  }
}

/* ---------- Infinite scroll (simulation) ---------- */
window.addEventListener("scroll", () => {
  const loader = document.getElementById("infiniteLoader");
  if (!loader) return;
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
  if (scrollTop + clientHeight >= scrollHeight - 200) {
    loader.style.opacity = "1";
    setTimeout(() => {
      // simulate loading more feed posts
    }, 1000);
  }
});

/* ---------- Auth & onboarding ---------- */
// Eye icon inside a password field: show/hide the typed password
function togglePasswordVisibility(btn) {
  const input = btn.previousElementSibling;
  if (!input) return;
  const showing = input.type === "text";
  input.type = showing ? "password" : "text";
  const icon = btn.querySelector("i");
  if (icon) icon.setAttribute("data-lucide", showing ? "eye" : "eye-off");
  if (typeof lucide !== "undefined") lucide.createIcons();
}

// Selectable "field / industry" chips on the profile form (multi-select)

function toggleFieldChip(button) {
  button.classList.toggle("is-selected");

  const selectedFields = [];

  document.querySelectorAll(".field-chip.is-selected").forEach((chip) => {
    selectedFields.push(chip.textContent.trim());
  });

  document.getElementById("selectedFields").value = selectedFields.join(",");
}

// Live preview for the avatar file picker on the profile form
function previewAvatar(input, imgId) {
  const file = input.files && input.files[0];
  if (!file) return;
  const img = document.getElementById(imgId);
  if (!img) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

/* ---------- Icons ---------- */
window.onload = function () {
  if (typeof lucide !== "undefined") lucide.createIcons();
};

document.addEventListener("DOMContentLoaded", function () {
  const loadingBtns = document.querySelectorAll(".btn-loading");
  loadingBtns.forEach((btn) => {
    const parentForm = btn.closest("form");


    if (parentForm) {
      parentForm.addEventListener("submit", function (e) {

        const btnTxt = btn.dataset.text;
        btn.dataset.originalHtml = btn.innerHTML;

        btn.innerHTML = `
                   <span class="spinner spinner-sm spinner--on-primary" role="status" aria-hidden="true"></span>
                    ${btnTxt} 
                `;
        btn.disabled = true;
      });
    }
  });

  // --- Back Button Error Fixer ---

  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      loadingBtns.forEach((button) => {
        if (button.dataset.originalHtml) {
          button.innerHTML = button.dataset.originalHtml;
        }
        button.disabled = false;
      });
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const messageElements = document.querySelectorAll("#django-messages div");

  messageElements.forEach((el) => {
    const message = el.getAttribute("data-message");
    let type = el.getAttribute("data-type");

    if (type === "error") {
      type = "info";
    }

    showToast(message, type);
  });
});