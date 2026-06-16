const modal = document.getElementById('modal-mascota');

function openModal(completed) {
  if (completed) {
    document.getElementById('modal-title').textContent = '🎉 ¡Tu compañero creció!';
    document.getElementById('modal-sub').textContent   = '¿Qué quieres criar ahora?';
  }
  modal.style.display = 'flex';
}
