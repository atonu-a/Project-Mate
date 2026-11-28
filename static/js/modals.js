// Project delete modal open
function openModal(slug) {
  const modal = document.getElementById(`delete-modal-${slug}`);
  if (!modal) return;
  modal.hidden = false;
}
// Project delete modal close
function closeModal(slug) {
  const modal = document.getElementById(`delete-modal-${slug}`);
  if (!modal) return;
  modal.hidden = true;
}

// join request message modal open
function openMsgModal(slug) {
  const modal = document.getElementById(`send-msg-modal-${slug}`);

  if (!modal) return;
  modal.hidden = false;
}

// send request msg modal close
function closeMsgModal(slug) {
  const modal = document.getElementById(`send-msg-modal-${slug}`);
  if (!modal) return;
  modal.hidden = true;
}

// Project leave modal open
function openLeaveModal(slug) {
  if (!modal) return;
  modal.hidden = false;
}
// Project leave modal close
function closeLeaveModal(slug) {
  const modal = document.getElementById(`leave-modal-${slug}`);
  if (!modal) return;
  modal.hidden = true;
}

// Request Cancel Modal
function openCancelReqModal(slug) {
  const modal = document.getElementById(`cancel-req-modal-${slug}`);
  if (!modal) return;
  modal.hidden = false;
}

function closeCancelReqModal(slug) {
  const modal = document.getElementById(`cancel-req-modal-${slug}`);
  if (!modal) return;
  modal.hidden = true;
}

// Teammate remove modal open
function openRemoveModal(slug) {
  const modal = document.getElementById(`remove-modal-${slug}`);
  if (!modal) return;
  modal.hidden = false;
}
// Teammate remove modal close
function closeRemoveModal(slug) {
  const modal = document.getElementById(`remove-modal-${slug}`);
  if (!modal) return;
  modal.hidden = true;
}

/* Delete account modal */
function openDeleteModal() {
  const modal = document.getElementById("deleteModal");
  if (!modal) return;
  modal.hidden = false;
  document.getElementById("deleteConfirmInput").focus();
}

function closeDeleteModal() {
  const modal = document.getElementById("deleteModal");
  if (!modal) return;
  modal.hidden = true;
  document.getElementById("deleteConfirmInput").value = "";
  checkDeleteInput();
}

function checkDeleteInput() {
  const input = document.getElementById("deleteConfirmInput");
  const btn = document.getElementById("deleteConfirmBtn");
  if (!input || !btn) return;
  btn.disabled = input.value.trim() !== DELETE_WORD;
}

document.addEventListener("keydown", (e) => {
  const modal = document.getElementById("deleteModal");
  if (e.key === "Escape" && modal && !modal.hidden) closeDeleteModal();
});

document.addEventListener("click", (e) => {
  if (e.target.id === "deleteModal") closeDeleteModal();
});

/* Account Privacy modal */
function openPrivacyModal() {
  const modal = document.getElementById("privacyModal");
  if (!modal) return;
  modal.hidden = false;
}
function closePrivacyModal() {
  const modal = document.getElementById("privacyModal");
  if (!modal) return;
  modal.hidden = true;
}

// Task Create Modal

function openTaskModal() {
  const modal =  document.getElementById("createTaskModal");
  modal.hidden = false;
  const project = document.getElementById("taskProject");
  if (project) loadProjectMembers(project.value);
}
function closeTaskModal() {
  const modal =  document.getElementById("createTaskModal");
  modal.hidden = true;
}

function loadProjectMembers(projectId) {
  const assignee = document.getElementById("taskAssignee");
  const dataElement = document.getElementById("project-members");
  if (!assignee || !dataElement) return;

  const projectMembers = JSON.parse(dataElement.textContent || "{}");
  const members = projectMembers[String(projectId)] || [];

  assignee.innerHTML = "";
  if (members.length === 0) {
    assignee.add(new Option("Select Project First", "", true, true));
    assignee.disabled = true;
    return;
  }

  assignee.disabled = false;
  assignee.add(new Option("Select a member", "", true, true));
  members.forEach((member) => {
    assignee.add(new Option(member.name, String(member.id)));
  });
}
