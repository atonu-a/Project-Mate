/* ---------- Like, Save Post Without Page Refreshing ---------- */
document.addEventListener("submit", async (e) => {
  const form = e.target;

  if (
    !form.classList.contains("like-form") &&
    !form.classList.contains("save-form") &&
    !form.classList.contains("comment-form") &&
    !form.classList.contains("reply-form")
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
          <button onclick="toggleReplyBox(this)" type="button" class="comment__action">Reply</button>
          <span class="comment__time">Just Now</span>
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



  // Reply Form Logic

  if (form.classList.contains("reply-form")) {

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
      const body = form.closest(".comment__body");
      const list = body?.querySelector(":scope > .comment__replies");
      if (!body || !list) {
        return;
      }

      const comment = document.createElement("div");
      comment.className = "comment comment--reply";

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
          <button onclick="toggleReplyBox(this)" type="button" class="comment__action">Reply</button>
          <span class="comment__time">Just Now</span>
        </div>
      </div>
    `;

      comment.querySelector(".comment__name").textContent =
        commentData.full_name;

      comment.querySelector(".comment__text").textContent =
        commentData.commented_text;

      list.prepend(comment);
      list.classList.remove("is-empty", "is-collapsed");

      let toggle = body.querySelector(":scope > .comment__toggle-replies");
      if (!toggle) {
        toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "comment__toggle-replies";
        toggle.addEventListener("click", () => toggleReplies(toggle));
        body.insertBefore(toggle, list);
      }

      const replyCount = Number(toggle.dataset.count || 0) + 1;
      toggle.dataset.count = replyCount;
      toggle.textContent = `Hide replies`;

      input.value = "";
      form.hidden = true;
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

// Reply System
function toggleReplyBox(btn) {
  const body = btn.closest(".comment__body");

  if (!body) return;

  const form = body.querySelector(".reply-form");

  if (!form) return;
  form.hidden = !form.hidden;
  if (!form.hidden) {
    const input = form.querySelector("input");
    input.focus();
  }
}

// "View 2 replies" / "Hide replies"
function toggleReplies(btn) {
  const replies = btn.parentElement.querySelector(":scope > .comment__replies");
  if (!replies) return;
  const collapsed = replies.classList.toggle("is-collapsed");
  btn.textContent = collapsed
    ? `View ${btn.dataset.count} replies`
    : "Hide replies";
}
