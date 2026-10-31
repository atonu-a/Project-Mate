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
/* ---------- Icons ---------- */
window.onload = function () {
  if (typeof lucide !== "undefined") lucide.createIcons();
};
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

/* ---------- Mobile Menu toggles ---------- */
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

/* ---------- Suggested Teammates Panel  ---------- */
function toggleSuggestedTeammates() {
  const panel = document.getElementById("suggestedTeammatesPanel");
  const toggle = document.querySelector(".feed-suggestions-toggle");
  if (!panel || !toggle) return;

  const isOpen = panel.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", String(isOpen));
  document.body.classList.toggle("suggestions-open", isOpen);

  if (isOpen) {
    panel.querySelector(".suggest-panel__close")?.focus();
  } else {
    toggle.focus();
  }
}

function closeSuggestedTeammates() {
  const panel = document.getElementById("suggestedTeammatesPanel");
  const toggle = document.querySelector(".feed-suggestions-toggle");
  if (!panel || !toggle || !panel.classList.contains("is-open")) return;

  panel.classList.remove("is-open");
  toggle.setAttribute("aria-expanded", "false");
  document.body.classList.remove("suggestions-open");
  toggle.focus();
}

/* ---------- Opening Global Search Button ---------- */
function openGlobalSearch() {
  const header = document.querySelector(".site-header__inner");
  const toggle = document.querySelector(".header-search__toggle");
  const input = document.getElementById("globalSearchInput");
  if (!header || !toggle || !input) return;

  header.classList.add("is-search-open");
  toggle.setAttribute("aria-expanded", "true");
  input.focus();
}

/* ---------- Closing Global Search Button ---------- */
function closeGlobalSearch() {
  const header = document.querySelector(".site-header__inner");
  const toggle = document.querySelector(".header-search__toggle");
  const input = document.getElementById("globalSearchInput");
  if (!header || !toggle || !input) return;

  header.classList.remove("is-search-open");
  toggle.setAttribute("aria-expanded", "false");
  input.value = "";
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeGlobalSearch();
    closeSuggestedTeammates();
  }
});

function switchSearchTab(tabBtn, panelId) {
  if (!tabBtn) return;
  const tabsWrap = tabBtn.closest(".search-tabs");
  const panelsWrap = tabsWrap ? tabsWrap.parentElement : document;

  if (tabsWrap) {
    tabsWrap
      .querySelectorAll(".search-tab")
      .forEach((t) => t.classList.remove("is-active"));
  }
  tabBtn.classList.add("is-active");

  panelsWrap
    .querySelectorAll(".search-panel")
    .forEach((p) => p.classList.remove("is-active"));
  const panel = document.getElementById(panelId);
  if (panel) panel.classList.add("is-active");
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

/* ---------- Like, Save Post Without Page Refreshing ---------- */
document.addEventListener("submit", async (e) => {
  const form = e.target;

  if (
    !form.classList.contains("like-form") &&
    !form.classList.contains("save-form") &&
    !form.classList.contains("comment-form")
  ) {
    return;
  }
  e.preventDefault();

  // Like Form Logic
  if (form.classList.contains("like-form")) {
    const response = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
      },
    });
    const data = await response.json();
    if (data.login_required) {
      window.location.href = data.login_url;
      return;
    }
    if (!data.success) {
      showToast(data.message);
      return;
    }
    const btn = form.querySelector(".reaction");
    const count = form.querySelector(".like-count");

    if (data.liked) {
      btn.classList.add("is-liked");
    } else {
      btn.classList.remove("is-liked");
    }
    if (data.likes_count == 0) {
      count.textContent = `Like`;
    } else if (data.likes_count == 1) {
      count.textContent = `${data.likes_count} like`;
    } else {
      count.textContent = `${data.likes_count} likes`;
    }
  }

  //  Save Form Logic
  if (form.classList.contains("save-form")) {
    const res = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
      },
    });
    const save_data = await res.json();
    if (save_data.login_required) {
      window.location.href = save_data.login_url;
      return;
    }

    if (!save_data.success) {
      showToast(save_data.message);
      return;
    }
    const save_btn = form.querySelector(".save-btn");
    if (save_data.saved) {
      showToast(save_data.msg);
      save_btn.innerHTML = `<i class="fa-solid fa-bookmark"></i> Unsave`;
    } else {
      showToast(save_data.msg);
      save_btn.innerHTML = `<i class="fa-regular fa-bookmark"></i> Save`;
    }
  }

  // Comment Form Logic

  if (form.classList.contains("comment-form")) {
    const input = form.querySelector(".comment-composer__input");
    const text = input.value.trim();

    if (!text) return;

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: new FormData(form),
      });

      const data = await response.json();

      if (data.login_required) {
        window.location.href = data.login_url;
        return;
      }

      if (!response.ok || !data.success) {
        showToast(data.error || "Comment could not be submitted.");
        return;
      }

      const commentData = data.comment;
      const list = form.nextElementSibling;

      if (!list) {
        console.error("Comment list not found.");
        return;
      }

      const comment = document.createElement("div");
      comment.className = "comment";

      comment.innerHTML = `
      <img
        src="${commentData.profile_pic || "/static/images/default-avatar.png"}"
        alt="${commentData.full_name}"
        class="comment__avatar"
      >
      <div class="comment__body">
        <div class="comment__bubble">
          <h4 class="comment__name"></h4>
          <p class="comment__text"></p>
        </div>
        <div class="comment__meta">

          <span class="comment__time">Now</span>
        </div>
      </div>
    `;

      comment.querySelector(".comment__name").textContent =
        commentData.full_name;

      comment.querySelector(".comment__text").textContent =
        commentData.commented_text;

      list.prepend(comment);

      input.value = "";
    } catch (error) {
      console.error("Comment submission failed:", error);
      showToast("Something went wrong. Please try again.");
    }
  }
});

// Timestamp formatting for comments
function formatCommentTime(timestamp) {
  const createdAt = new Date(timestamp);
  const now = new Date();

  const diffMs = now - createdAt;
  const diffHours = diffMs / (1000 * 60 * 60);
  const diffDays = Math.floor(diffHours / 24);

  if (Number.isNaN(createdAt.getTime()) || diffMs < 0) {
    return "";
  }

  if (diffHours < 24) {
    return createdAt.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  }

  if (diffDays <= 7) {
    return `${diffDays}d`;
  }

  return createdAt.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

/* ---------- Opening Comment Section ---------- */
function toggleComments(btn) {
  const post = btn.closest(".post");
  if (!post) return;
  const panel = post.querySelector(".post__comments");
  if (!panel) return;

  panel.classList.toggle("is-open");

  if (panel.classList.contains("is-open")) {
    const input = panel.querySelector(".comment-composer__input");
    if (input) input.focus();
  }
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

// Opening Preloader
// window.addEventListener("load", () => {
//   try {
//     const preloader = document.getElementById("preloader");

//     // Add the hidden class to trigger the smooth CSS transition
//     preloader.classList.add("preloader-hidden");

//     // Optional: Completely remove the element from the DOM after the animation finishes
//     setTimeout(() => {
//       preloader.remove();
//     }, 500);
//   } catch {}
// });

const preloader = document.getElementById("preloader");

if (!sessionStorage.getItem("introShown")) {
  window.addEventListener("load", function () {
    setTimeout(() => {
      preloader.classList.add("hide");
      sessionStorage.setItem("introShown", "true");
    }, 2000);
  });
} else {
  preloader.classList.add("hide");
}

// Loading buttons
document.addEventListener("DOMContentLoaded", function () {
  const loadingBtns = document.querySelectorAll(".btn-loading");
  loadingBtns.forEach((btn) => {
    const parentForm = btn.closest("form");

    if (parentForm) {
      parentForm.addEventListener("submit", function (e) {
        const btnTxt = btn.dataset.text || btn.textContent.trim() || "Loading";
        btn.dataset.originalHtml = btn.innerHTML;

        btn.innerHTML = `
                   <span class="spinner spinner--sm spinner--on-primary" role="status" aria-hidden="true"></span>
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

/* ---------- Messages (mobile list / conversation toggle) ---------- */
// Tapping a conversation in the list: mark it active, reflect the person in
// the open conversation's header, and (on phones) swap from the list view
// to the conversation view.
function openConversation(item) {
  const chat = item.closest(".chat");
  if (!chat) return;

  chat
    .querySelectorAll(".chat__item")
    .forEach((i) => i.classList.remove("is-active"));
  item.classList.add("is-active");

  const name = item.dataset.name;
  const avatar = item.dataset.avatar;
  const status = item.dataset.status;

  if (name) {
    const nameEl = chat.querySelector(".chat__peer-name");
    if (nameEl) nameEl.textContent = name;
  }
  if (avatar) {
    chat.querySelectorAll(".chat__peer-avatar").forEach((img) => {
      img.src = avatar;
    });
  }
  if (status) {
    const statusEl = chat.querySelector(".chat__peer-status");
    // Keep the little status dot; only replace the trailing text node.
    if (statusEl && statusEl.lastChild) statusEl.lastChild.textContent = status;
  }

  chat.classList.add("is-chat-open");
}
// Message sending
// try {
//   const sendMsg = document.getElementById("send-msg");
//   console.log("Clicked")
//   sendMsg.addEventListener("click",() => {
//     setTimeout(()=> {
//       sendMsg.disabled = true;
//       sendMsg.innerText = "sent";
//     },10000)
//   })
// } catch (error) {
//
// }

// Back button in the conversation header: return to the list on phones.
function closeConversation(btn) {
  const chat = btn.closest(".chat");
  if (chat) chat.classList.remove("is-chat-open");
}

/* ---------- Checking Request Button ---------- */
try {
  const btnDone = document.querySelectorAll(".btn-check");
  btnDone.forEach((btn) => {
    btn.addEventListener("click", () => {
      const btnTxt = btn.dataset.text || btn.textContent.trim() || "";
      const btnTxtDefault = btn.innerText;
      btn.dataset.originalHtml = btn.innerHTML;
      btn.classList.remove("btn-primary");
      btn.classList.add("btn-secondary");

      btn.innerHTML = `
                   <i class="fa-solid fa-check"></i>
                    ${btnTxt}
                `;
      btn.disabled = true;

      setTimeout(() => {
        btn.classList.remove("btn-secondary");
        btn.classList.add("btn-primary");
        btn.innerHTML = btnTxtDefault;
        btn.disabled = false;
      }, 30000);
    });
  });
} catch (error) {
  console.log("not clicked");
}

// Profile buttons show-hide system (whatsapp ,linkedin etc)
try {
  const btnDown = document.getElementById("btn-down");
  const extraItems = document.getElementById("extra-items");

  btnDown.addEventListener("click", () => {
    btnDown.classList.toggle("btn-up");
    extraItems.classList.toggle("hide");
  });
} catch (error) {}

// Profile image editing
try {
  // Cropper & Preview State
  let cropperInstance = null;
  let currentPreviewId = null;

  // Original File Reference Storage
  const originalFiles = {
    editAvatarPreview: null,
    editCoverPreview: null,
  };

  function previewAvatar(input, previewId) {
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const preview = document.getElementById(previewId);
        if (preview instanceof HTMLImageElement) {
          preview.src = e.target.result;
        } else if (preview) {
          preview.style.backgroundImage = `url("${e.target.result}")`;
          preview.style.backgroundSize = "cover";
          preview.style.backgroundPosition =
            preview.style.objectPosition || "center";
        }
      };
      reader.readAsDataURL(file);
    }
  }
} catch (error) {}

// Show and hide of payment details
function toggleDetails() {
  const compensation_type = document.getElementById("compensation").value;
  const paymentBox = document.getElementById("payment-details-box");
  const amount = document.getElementById("payment-details");

  if (compensation_type == "Paid") {
    paymentBox.style.display = "block";
    amount.required = true;
  } else {
    paymentBox.style.display = "none";
    amount.required = false;
    amount.value = "";
  }
}

function initializePaymentDetails() {
  if (document.getElementById("compensation")) {
    toggleDetails();
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializePaymentDetails, {
    once: true,
  });
} else {
  initializePaymentDetails();
}

// Project More Option
try {
  const containers = document.querySelectorAll(".post-more-container");

  containers.forEach((container) => {
    const btn = container.querySelector("button");
    const dropdown = container.querySelector(".three-dot-dropdown");
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      dropdown.classList.toggle("hide");
    });

    document.addEventListener("click", () => {
      dropdown.classList.add("hide");
    });
  });
} catch (error) {}


function removeFromSaved(btn) {
  const card = btn.closest(".spotlight-card");
  if (!card) return;

  card.style.transition = "opacity 0.2s, transform 0.2s";
  card.style.opacity = "0";
  card.style.transform = "scale(0.96)";

  setTimeout(() => card.remove(), 200);
  showToast("Removed from saved projects", "info");
}

// Copy LInk

document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".copy-link-btn");

  if (!btn) return;

  const url = btn.dataset.url;

  try {
    await navigator.clipboard.writeText(
      new URL(url, window.location.origin).href,
    );

    showToast("Link copied to clipboard!");
  } catch (error) {
    showToast("Unable to copy link. Please try again.");
    console.error("Clipboard error:", error);
  }
});

function toggleFaq(btn) {
  const item = btn.closest(".faq-item");
  if (item) item.classList.toggle("is-open");
}