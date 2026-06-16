const POOL = {
  logro:   ['🎉 ¡Increíble, sigue así!', '🚀 ¡Eres imparable!', '⚡ ¡Achievement desbloqueado!',
            '🔥 ¡Máquina de victorias!', '💪 ¡Eso es dedicación pura!', '🏆 ¡Un paso más hacia la cima!'],
  proceso: ['🌱 ¡Cada experto fue principiante!', '🧠 ¡Aprender es el superpoder más grande!',
            '⚙️ ¡El progreso constante vence al talento!', '📚 ¡Un día de práctica más, un nivel ganado!'],
  subio:   ['📈 ¡Vamos por más, no pares ahora!', '🚀 ¡Nivel arriba! ¡El techo no existe!',
            '🔥 ¡Eso es crecimiento real, sigue empujando!', '💥 ¡Subiste de nivel como un pro!'],
  bajo:    ['💪 ¡Los tropiezos son parte del camino!', '🌊 ¡Hasta los mejores retroceden para tomar impulso!',
            '🧩 ¡Revisar la base es de valientes!', '🌱 ¡Cada paso atrás es una lección disfrazada!'],
};

function rand(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function showMessage(pool) {
  const el = document.getElementById('celebracion-msg');
  el.textContent = rand(pool);
  el.classList.add('visible');
  setTimeout(() => el.classList.remove('visible'), 3200);
}
