// Project delete modal open
function openModal(slug) {
  const modal = document.getElementById(`delete-modal-${slug}`);
  if (modal) {
    modal.style.display = "block";
  } else {
  }
}
// Project delete modal close
function closeModal(slug) {
  const modal = document.getElementById(`delete-modal-${slug}`);
  if (modal) {
    modal.style.display = "none";
  }
}

// join request message modal open
function openMsgModal(slug) {
  const modal = document.getElementById(`send-msg-modal-${slug}`);

  if (modal) {
    modal.style.display = "block";

  }
}

// send request msg modal close
function closeMsgModal(slug) {
  const modal = document.getElementById(`send-msg-modal-${slug}`);
  if (modal) {
    modal.style.display = "none";
  }
}



// Project leave modal open
function openLeaveModal(slug) {
  const modal = document.getElementById(`leave-modal-${slug}`);
  if (modal) {
    modal.style.display = "block";
  }
}
// Project leave modal close
function closeLeaveModal(slug) {
  const modal = document.getElementById(`leave-modal-${slug}`);
  if (modal) {
    modal.style.display = "none";
  } else {
  }
}


// Request Cancel Modal
function openCancelReqModal(slug) {
  const modal = document.getElementById(`cancel-req-modal-${slug}`);
  if (modal) {
    modal.style.display = "block";
  }
}

function closeCancelReqModal(slug) {
  const modal = document.getElementById(`cancel-req-modal-${slug}`);
  if (modal) {
    modal.style.display = "none";
  }
}

// Teammate remove modal open
function openRemoveModal(slug) {
  const modal = document.getElementById(`remove-modal-${slug}`);
  if (modal) {
    modal.style.display = "block";
  }
}
// Teammate remove modal close
function closeRemoveModal(slug) {
  const modal = document.getElementById(`remove-modal-${slug}`);
  if (modal) {
    modal.style.display = "none";
  } else {
  }
}