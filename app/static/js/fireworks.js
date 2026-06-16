function launchFireworks() {
  const canvas = document.getElementById('fireworks-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  canvas.style.display = 'block';
  const colors = ['#7c3aed', '#06b6d4', '#f59e0b', '#22c55e', '#f97316', '#ec4899', '#fff'];
  const particles = [];

  function burst(x, y) {
    for (let i = 0; i < 90; i++) {
      const a = (Math.PI * 2 * i) / 90;
      const s = Math.random() * 7 + 2;
      particles.push({
        x, y,
        vx: Math.cos(a) * s,
        vy: Math.sin(a) * s,
        alpha: 1,
        color: colors[Math.floor(Math.random() * colors.length)],
        size: Math.random() * 4 + 1.5,
      });
    }
  }

  [[0.25, 0.3], [0.75, 0.25], [0.5, 0.45], [0.15, 0.55], [0.85, 0.5]]
    .forEach(([px, py], i) => setTimeout(() => burst(px * canvas.width, py * canvas.height), i * 280));

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.vy += 0.12; p.vx *= 0.99; p.alpha -= 0.014;
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1;
    for (let i = particles.length - 1; i >= 0; i--) {
      if (particles[i].alpha <= 0) particles.splice(i, 1);
    }
    if (particles.length > 0) requestAnimationFrame(animate);
    else canvas.style.display = 'none';
  }

  animate();
}
