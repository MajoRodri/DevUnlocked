const primeraVez = window.APP_DATA.primeraVez;
const params     = new URLSearchParams(window.location.search);
const nuevo      = params.get('nuevo');
const cambio     = params.get('cambio');
const completado = params.get('completado');

if (primeraVez) {
  openModal(false);
} else if (completado === '1') {
  launchFireworks();
  openModal(true);
}

if (nuevo === 'logro' || nuevo === 'proceso') {
  if (!completado) launchFireworks();
  showMessage(POOL[nuevo]);
  if (!completado) window.history.replaceState({}, '', '/');
} else if (cambio === 'subio') {
  if (!completado) launchFireworks();
  showMessage(POOL.subio);
  if (!completado) window.history.replaceState({}, '', '/');
} else if (cambio === 'bajo') {
  showMessage(POOL.bajo);
  window.history.replaceState({}, '', '/');
}
