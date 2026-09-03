/* scrollfx.js — kleine Scroll-Engine für Redesign-Mockups (stemago-tools /redesign-studio).
 * Einbinden: <script src="../scrollfx.js" defer></script> (relativ zu design/mockups/<richtung>/index.html)
 *
 * Attribute
 *   data-reveal            blendet ein, sobald das Element in den Viewport kommt (Klasse .is-visible);
 *                          data-reveal="words" zerlegt den Text in <span class="fx-word" style="--i:n"> für Wort-Reveals
 *   data-parallax="0.2"    verschiebt das Element um Faktor × Abstand zur Viewport-Mitte (translateY)
 *   data-scene             Sticky-Szene: setzt --p (0..1) = Fortschritt des Elements durch den Viewport;
 *                          Kinder lesen var(--p), z.B. transform: translateX(calc(var(--p) * -40vw))
 *   data-counter="1200"    zählt von 0 auf den Wert, sobald sichtbar; data-counter-suffix="+" optional
 *   data-tilt              leichte 3D-Neigung beim Hover
 *
 * prefers-reduced-motion: Reveals sofort sichtbar, kein Parallax/Tilt, Zähler auf Endwert, --p = 1.
 * Verifier: window.scrollfx.setProgress(sceneEl, p) setzt --p manuell für Screenshots.
 *
 * Basis-CSS (ins Mockup übernehmen):
 *   [data-reveal] { opacity: 0; transform: translateY(16px); transition: opacity .6s ease, transform .6s ease; }
 *   [data-reveal].is-visible { opacity: 1; transform: none; }
 *   .fx-word { display: inline-block; opacity: 0; transform: translateY(.4em);
 *              transition: opacity .5s ease calc(var(--i) * 40ms), transform .5s ease calc(var(--i) * 40ms); }
 *   .is-visible .fx-word { opacity: 1; transform: none; }
 *   @media (prefers-reduced-motion: reduce) { [data-reveal], .fx-word { opacity: 1; transform: none; transition: none; } }
 */
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const all = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const clamp = (v) => Math.min(1, Math.max(0, v));

  // --- reveal -------------------------------------------------------------
  const reveals = all('[data-reveal]');
  reveals.forEach((el) => {
    if (el.dataset.reveal === 'words') {
      const words = el.textContent.trim().split(/\s+/);
      el.textContent = '';
      words.forEach((w, i) => {
        const span = document.createElement('span');
        span.className = 'fx-word';
        span.style.setProperty('--i', String(i));
        span.textContent = w;
        el.appendChild(span);
        if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
      });
    }
  });
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('is-visible'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    reveals.forEach((el) => io.observe(el));
  }

  // --- counters -----------------------------------------------------------
  const fmt = (n) => n.toLocaleString('de-DE');
  const counters = all('[data-counter]');
  const finish = (el) => { el.textContent = fmt(parseFloat(el.dataset.counter) || 0) + (el.dataset.counterSuffix || ''); };
  const run = (el) => {
    const end = parseFloat(el.dataset.counter) || 0;
    const suffix = el.dataset.counterSuffix || '';
    const dur = 1200;
    const t0 = performance.now();
    const step = (t) => {
      const k = clamp((t - t0) / dur);
      const v = Math.round(end * (1 - Math.pow(1 - k, 3)));
      el.textContent = fmt(v) + suffix;
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (reduce || !('IntersectionObserver' in window)) {
    counters.forEach(finish);
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach((el) => io.observe(el));
  }

  // --- scenes + parallax (scroll-driven) ----------------------------------
  const scenes = all('[data-scene]');
  const paras = all('[data-parallax]');
  const setProgress = (el, p) => { el.style.setProperty('--p', clamp(p).toFixed(4)); };
  const update = () => {
    const vh = window.innerHeight;
    scenes.forEach((el) => {
      const r = el.getBoundingClientRect();
      const total = r.height - vh;
      setProgress(el, total > 0 ? -r.top / total : (r.top <= 0 ? 1 : 0));
    });
    paras.forEach((el) => {
      const f = parseFloat(el.dataset.parallax);
      const factor = Number.isFinite(f) ? f : 0.2;
      const r = el.getBoundingClientRect();
      const centerOffset = r.top + r.height / 2 - vh / 2;
      el.style.transform = 'translate3d(0, ' + (-centerOffset * factor).toFixed(1) + 'px, 0)';
    });
  };
  if (reduce) {
    scenes.forEach((el) => setProgress(el, 1));
  } else {
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { update(); ticking = false; });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  // --- tilt ---------------------------------------------------------------
  if (!reduce) {
    all('[data-tilt]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(800px) rotateX(' + (-y * 6).toFixed(2) + 'deg) rotateY(' + (x * 6).toFixed(2) + 'deg)';
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  window.scrollfx = { setProgress, update, reduce };
})();
