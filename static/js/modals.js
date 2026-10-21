// Project delete modal open
function openModal(slug) {
  const modal = document.getElementById(`delete-modal-${slug}`);
    console.log("got it");
  if (modal) {
    modal.style.display = "block";
    console.log("modal opened");
  } else {
    console.log("modal not found");
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
    console.log("got it");
  if (modal) {
    modal.style.display = "none";
        console.log("modal opened");
  } else {
    console.log("modal not found");
  }
}