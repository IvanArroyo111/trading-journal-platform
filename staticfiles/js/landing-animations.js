// Fade-in animation for hero, stats, and features sections
document.addEventListener('DOMContentLoaded', function () {
  // Reveal main sections
  ['.hero-content', '.stats-bar', '.features-section'].forEach(selector => {
    const el = document.querySelector(selector);
    if (el) el.classList.add('visible');
  });

  // Staggered reveal for feature cards
  document.querySelectorAll('.feature-card').forEach((el, i) => {
    setTimeout(() => el.classList.add('visible'), 300 + i * 120);
  });

  // --- Animated Stars ---
  function animateStars() {
    const canvas = document.querySelector('.hero-stars-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w = canvas.width = canvas.offsetWidth;
    let h = canvas.height = canvas.offsetHeight;
    let stars = [];
    const STAR_COUNT = Math.floor(w * 0.18);

    // Generate a random star object
    function randomStar() {
      return {
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.2 + 0.4,
        alpha: Math.random() * 0.6 + 0.2,
        twinkle: Math.random() * 2 * Math.PI,
        speed: Math.random() * 0.15 + 0.03,
        float: Math.random() * 0.8 + 0.2
      };
    }

    // Resize canvas and regenerate stars on window resize
    function resize() {
      w = canvas.width = canvas.offsetWidth;
      h = canvas.height = canvas.offsetHeight;
      stars = [];
      for (let i = 0; i < STAR_COUNT; i++) stars.push(randomStar());
    }
    window.addEventListener('resize', resize);

    // Draw stars with twinkle animation
    function draw() {
      ctx.clearRect(0, 0, w, h);
      for (let s of stars) {
        s.twinkle += s.speed * 0.7;
        let a = s.alpha + Math.sin(s.twinkle) * 0.18;
        ctx.save();
        ctx.globalAlpha = Math.max(0, Math.min(1, a));
        ctx.beginPath();
        ctx.arc(s.x, s.y + Math.sin(s.twinkle) * s.float * 2, s.r, 0, 2 * Math.PI);
        ctx.fillStyle = "#fff";
        ctx.shadowColor = "#00e6d0";
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.restore();
      }
      requestAnimationFrame(draw);
    }
    resize();
    draw();
  }

  // --- Animated Particles ---
  function animateParticles() {
    const canvas = document.querySelector('.hero-particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w = canvas.width = canvas.offsetWidth;
    let h = canvas.height = canvas.offsetHeight;
    let particles = [];
    const PARTICLE_COUNT = Math.floor(w * 0.12);

    // Generate a random particle object
    function randomParticle() {
      const isSparkle = Math.random() > 0.7;
      return {
        x: Math.random() * w,
        y: Math.random() * h,
        r: isSparkle ? Math.random() * 1.8 + 0.8 : Math.random() * 2.5 + 1.2,
        alpha: Math.random() * 0.3 + 0.15,
        dx: (Math.random() - 0.5) * 0.18,
        dy: (Math.random() - 0.5) * 0.18,
        baseAlpha: Math.random() * 0.3 + 0.15,
        sparkle: isSparkle,
        t: Math.random() * 2 * Math.PI,
        speed: Math.random() * 0.008 + 0.004
      };
    }

    // Resize canvas and regenerate particles on window resize
    function resize() {
      w = canvas.width = canvas.offsetWidth;
      h = canvas.height = canvas.offsetHeight;
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(randomParticle());
    }
    window.addEventListener('resize', resize);

    // Draw particles with sparkle and movement animation
    function draw() {
      ctx.clearRect(0, 0, w, h);
      for (let p of particles) {
        p.x += p.dx;
        p.y += p.dy;
        p.t += p.speed;
        if (p.sparkle) {
          p.alpha = p.baseAlpha + Math.abs(Math.sin(p.t)) * 0.35;
        }
        // Wrap around edges
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;
        ctx.save();
        ctx.globalAlpha = Math.max(0, Math.min(1, p.alpha));
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, 2 * Math.PI);
        ctx.fillStyle = p.sparkle ? "#00e6d0" : "#fff";
        ctx.shadowColor = p.sparkle ? "#00e6d0" : "#fff";
        ctx.shadowBlur = p.sparkle ? 10 : 4;
        ctx.fill();
        ctx.restore();
      }
      requestAnimationFrame(draw);
    }
    resize();
    draw();
  }

  // Initialize animations
  animateStars();
  animateParticles();
});