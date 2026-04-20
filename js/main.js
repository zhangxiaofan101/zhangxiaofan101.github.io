/* ── Email spam protection ─────────────────────────────
   The address is never written in plain text in the HTML.
   Bots scraping static markup won't find it.
   ──────────────────────────────────────────────────── */
(function () {
  const u = 'xiaofan.zhang';
  const d = 'sjtu.edu.cn';
  const addr = u + '@' + d;

  document.querySelectorAll('[data-email]').forEach(el => {
    el.href = 'mailto:' + addr;
    el.title = addr;
  });
})();

/* ── Highlight active nav link ─────────────────────── */
(function () {
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path || (path === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
})();
