/* ═══════════════════════════════════════════════════════
   AURA STORAGE — Global JS
   Particles · Ambient glow · Nav scroll · Tabs · Utils
═══════════════════════════════════════════════════════ */

// ── Ambient glow (mouse follow) ──────────────────────────
const glow = document.getElementById('ambientGlow');
if (glow) {
  document.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top  = e.clientY + 'px';
  });
}

// ── Nav scroll state ─────────────────────────────────────
const nav = document.querySelector('.nav');
if (nav) {
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ── Particle system ──────────────────────────────────────
(function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, particles = [];
  const COUNT = 60;

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  function rand(min, max) { return Math.random() * (max - min) + min; }

  function spawn() {
    return {
      x: rand(0, W), y: rand(0, H),
      vx: rand(-0.15, 0.15), vy: rand(-0.25, -0.05),
      r: rand(0.5, 1.8),
      alpha: rand(0.05, 0.25),
      life: rand(0.005, 0.012),
      a: rand(0, 0.25),
    };
  }

  for (let i = 0; i < COUNT; i++) {
    const p = spawn();
    p.y = rand(0, H); // scatter vertically on init
    particles.push(p);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach((p, i) => {
      p.x  += p.vx;
      p.y  += p.vy;
      p.a  += p.life;
      const alpha = Math.sin(p.a * Math.PI) * p.alpha;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(78,205,196,${Math.max(0, alpha)})`;
      ctx.fill();
      if (p.a >= 1 || p.y < -10) particles[i] = spawn();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();

// ── Tab system ───────────────────────────────────────────
function initTabs(containerSelector) {
  document.querySelectorAll(containerSelector || '.tabs').forEach(tabBar => {
    tabBar.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.dataset.tab;
        const root = tabBar.closest('.tab-root') || document;

        tabBar.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        root.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        const panel = root.querySelector(`[data-panel="${target}"]`);
        if (panel) panel.classList.add('active');
      });
    });
  });
}
initTabs();

// ── Scroll reveal ────────────────────────────────────────
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('revealed'); revealObs.unobserve(e.target); }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

// ── Utility helpers ──────────────────────────────────────
window.AURA = {
  // Format numbers
  fmt: (n, dec = 1) => Number(n).toFixed(dec),
  fmtPct: (n) => Number(n).toFixed(1) + '%',
  fmtX: (n) => Number(n).toFixed(2) + '×',

  // Show alert
  showAlert(container, type, icon, msg) {
    const el = document.querySelector(container);
    if (!el) return;
    el.innerHTML = `<div class="alert alert-${type}"><span class="alert-icon">${icon}</span><span>${msg}</span></div>`;
  },

  // Fetch wrapper
  async post(url, body) {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return r.json();
  },

  async get(url) {
    const r = await fetch(url);
    return r.json();
  },

  // Animate a number from 0 to val
  animateVal(el, val, suffix = '', dec = 0, duration = 900) {
    if (!el) return;
    const start = performance.now();
    const update = (now) => {
      const t = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - t, 3);
      el.textContent = (val * ease).toFixed(dec) + suffix;
      if (t < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  },

  // Progress bar
  setProgress(selector, pct) {
    const el = document.querySelector(selector);
    if (el) el.style.width = Math.min(100, Math.max(0, pct)) + '%';
  },

  // Color for power state
  stateColor(state) {
    const map = { Active: '#E31E24', Idle: '#ff6b6b', 'Light Sleep': '#4ECDC4', 'Deep Sleep': '#a78bfa' };
    return map[state] || '#fff';
  },
  statePower(state) {
    const map = { Active: 2.3, Idle: 1.2, 'Light Sleep': 0.5, 'Deep Sleep': 0.1 };
    return map[state] ?? 0.1;
  },
};

// ── Upload drag-over effect ───────────────────────────────
document.querySelectorAll('.upload-zone').forEach(zone => {
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
  zone.addEventListener('drop', e => { e.preventDefault(); zone.classList.remove('drag-over'); });
});
