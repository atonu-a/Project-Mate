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

/* ---------- Icons ---------- */
window.onload = function () {
  if (typeof lucide !== "undefined") lucide.createIcons();
};

// Preloader
window.addEventListener("load", () => {
  try {
    const preloader = document.getElementById("preloader");

    // Add the hidden class to trigger the smooth CSS transition
    preloader.classList.add("preloader-hidden");

    // Optional: Completely remove the element from the DOM after the animation finishes
    setTimeout(() => {
      preloader.remove();
    }, 500);
  } catch {}
});

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

// User following
try {
  function toggleFollow(btn) {
    const following = btn.classList.toggle("btn-secondary");
    const icon = btn.querySelector("i");
    const label = btn.querySelector("span");
    if (icon)
      icon.setAttribute("data-lucide", following ? "user-check" : "user-plus");
    if (label) label.textContent = following ? "Following" : "Follow";
    if (typeof lucide !== "undefined") lucide.createIcons();
    showToast(following ? "You are now following this user" : "Unfollowed");
  }

  function copyProfileLink(btn) {
    navigator.clipboard
      .writeText(window.location.href)
      .then(() => showToast("Profile link copied!"))
      .catch(() => showToast("Could not copy link", "info"));
  }
} catch (error) {
  ;
}

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
  ;
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
} catch (error) {
  ;
}

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
        document.getElementById(previewId).src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  // // Function to open crop modal (Accepts both File Object and URL String)
  // function openCropModal(fileOrUrl, imgId) {
  //   if (!fileOrUrl) return;

  //   currentPreviewId = imgId;
  //   const modal = document.getElementById("cropModal");
  //   const imageToCrop = document.getElementById("imageToCrop");

  //   if (!modal || !imageToCrop) return;

  //   // Show modal first so dimensions are non-zero
  //   modal.style.display = "flex";

  //   const initCropperWithSrc = (src) => {
  //     if (cropperInstance) {
  //       cropperInstance.destroy();
  //       cropperInstance = null;
  //     }

  //     imageToCrop.src = src;

  //     // Calculate aspect ratio
  //     let ratio = 1;
  //     if (imgId === "editCoverPreview") {
  //       const targetImg = document.getElementById(imgId);
  //       if (targetImg && targetImg.clientHeight > 0) {
  //         ratio = targetImg.clientWidth / targetImg.clientHeight;
  //       } else {
  //         ratio = 16 / 9;
  //       }
  //     }

  //     cropperInstance = new Cropper(imageToCrop, {
  //       aspectRatio: ratio,
  //       viewMode: 1,
  //       autoCropArea: 1,
  //       responsive: true,
  //       restore: false
  //     });
  //   };

  //   if (typeof fileOrUrl === 'string') {
  //     // If string URL (e.g., loaded from server after save/refresh)
  //     initCropperWithSrc(fileOrUrl);
  //   } else {
  //     // If raw File Object (new upload)
  //     const reader = new FileReader();
  //     reader.onload = (e) => {
  //       initCropperWithSrc(e.target.result);
  //     };
  //     reader.readAsDataURL(fileOrUrl);
  //   }
  // }

  // // Close Modal Helper
  // function closeCropModal() {
  //   const modal = document.getElementById("cropModal");
  //   if (modal) {
  //     modal.style.display = "none";
  //   }
  //   if (cropperInstance) {
  //     cropperInstance.destroy();
  //     cropperInstance = null;
  //   }
  // }

  // // DOM Event Bindings
  // document.addEventListener("DOMContentLoaded", () => {
  //   // Preview Image Click Event Binding
  //   ["editAvatarPreview", "editCoverPreview"].forEach((imgId) => {
  //     const img = document.getElementById(imgId);
  //     if (img) {
  //       img.style.cursor = "pointer";

  //       img.addEventListener("click", () => {
  //         // Priority 1: User newly uploaded raw file
  //         if (originalFiles[imgId]) {
  //           openCropModal(originalFiles[imgId], imgId);
  //         }
  //         // Priority 2: Existing saved image URL from server
  //         else if (img.src && !img.src.includes('data:image')) {
  //           openCropModal(img.src, imgId);
  //         }
  //       });
  //     }
  //   });

  //   // Crop Apply Button
  //   const applyBtn = document.getElementById("applyCropBtn");
  //   if (applyBtn) {
  //     applyBtn.addEventListener("click", () => {
  //       if (!cropperInstance || !currentPreviewId) return;

  //       const canvas = cropperInstance.getCroppedCanvas();
  //       if (canvas) {
  //         const previewImg = document.getElementById(currentPreviewId);
  //         if (previewImg) {
  //           previewImg.src = canvas.toDataURL();
  //         }
  //       }
  //       closeCropModal();
  //     });
  //   }

  //   // Crop Cancel Button
  //   const cancelBtn = document.getElementById("cancelCropBtn");
  //   if (cancelBtn) {
  //     cancelBtn.addEventListener("click", closeCropModal);
  //   }
  // });
} catch (error) {
  ;
}

// Show and hide of payment details
function toggleDetails() {
  console.log("function exicuted!")
  const compensation_type = document.getElementById("compensation").value;
  const paymentBox = document.getElementById("payment-details-box");
  const amount = document.getElementById("payment-details");

  if (compensation_type == "Paid") {
    console.log("paid")
    paymentBox.style.display = "block";
    amount.required = true;
  } else {
    console.log("others")
    paymentBox.style.display = "none";
    amount.required = false;
    amount.value = "";
  }
}


// // Project detalis checking
// try{
//   const projectImgBox = document.querySelectorAll(".project-img");
  
//   projectImgBox.forEach((img) => {
//     img.addEventListener("mouseenter", () => {
//       const checkdetails = img.querySelector(".check-details-btn");
//       checkdetails.classList.remove("hide");
//     });
//     img.addEventListener("mouseleave", () => {
//       const checkdetails = img.querySelector(".check-details-btn");
//       checkdetails.classList.add("hide");
//     });
//   });
// }
// catch (error){
//   
// }



// Project More Option
try{
  const containers = document.querySelectorAll(".post-more-container");

  containers.forEach((container) => {
    const btn = container.querySelector("button");
    const dropdown = container.querySelector(".three-dot-dropdown")
    btn.addEventListener("click", (e)=>{ 
      e.stopPropagation();
      dropdown.classList.toggle("hide");

    })

    document.addEventListener("click", () => {
      dropdown.classList.add("hide");
    });
  });
}

catch(error){
  
}


// Project delete modal open
function openModal(slug){
  const modal = document.getElementById(`delete-modal-${slug}`);
  if (modal){
    modal.style.display = "block";
  }
}
// Project delete modal close
function closeModal(slug){
  const modal = document.getElementById(`delete-modal-${slug}`);
  if (modal){
    modal.style.display = "none";
  }
}

