let currentEditId = null;
let currentDeleteId = null;

// Delete modal functions
function openDeleteModal(id, name) {
  currentDeleteId = id;

  const deleteBtn = document.getElementById("confirmDeleteBtn");
  deleteBtn.href = `/delete/${id}`;

  const dialogTitle = document.getElementById("dialog-title");
  dialogTitle.textContent = `Delete ${name}'s birthday`;

  document.getElementById("deleteModal").classList.remove("hidden");
  document.getElementById("deleteModal").classList.add("flex");
}

function closeDeleteModal() {
  document.getElementById("deleteModal").classList.add("hidden");
  document.getElementById("deleteModal").classList.remove("flex");
  currentDeleteId = null;
}

// Close modals when clicking outside
document.getElementById("deleteModal").addEventListener("click", function (e) {
  if (e.target === this) closeDeleteModal();
});

// Add some interactive particles effect
function createParticle() {
  const particle = document.createElement("div");
  particle.className =
    "fixed w-2 h-2 bg-blue-400 rounded-full opacity-30 pointer-events-none z-10";
  particle.style.left = Math.random() * window.innerWidth + "px";
  particle.style.top = window.innerHeight + "px";
  particle.style.animation = "float 8s linear infinite";

  document.body.appendChild(particle);

  setTimeout(() => particle.remove(), 8000);
}

// Create particles periodically
setInterval(createParticle, 3000);
