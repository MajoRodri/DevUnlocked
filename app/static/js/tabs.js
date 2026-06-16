document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const tipo = tab.dataset.tipo;
    document.getElementById('tipo-input').value = tipo;
    document.getElementById('nivel-row').style.display = tipo === 'proceso' ? 'flex' : 'none';
    document.getElementById('logro').placeholder = tipo === 'proceso'
      ? 'Ej: Aprendiendo Python...'
      : 'Escribe tu logro del día...';
  });
});
